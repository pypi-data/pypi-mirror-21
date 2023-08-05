#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Core functionality
==================
.. autosummary::
    :toctree: generated/

    Pump
    transform
'''

import librosa
import jams

from .exceptions import ParameterError
from .task import BaseTaskTransformer
from .feature import FeatureExtractor
from .sampler import Sampler


def transform(audio_f, jam, *ops):
    '''Apply a set of operations to a track

    Parameters
    ----------
    audio_f : str
        The path to the audio file

    jam : str, jams.JAMS, or file-like
        A JAMS object, or path to a JAMS file.

        If not provided, an empty jams object will be created.

    ops : list of task.BaseTaskTransform or feature.FeatureExtractor
        The operators to apply to the input data

    Returns
    -------
    data : dict
        Extracted features and annotation encodings
    '''

    # Load the audio
    y, sr = librosa.load(audio_f, sr=None, mono=True)

    if jam is None:
        jam = jams.JAMS()
        jam.file_metadata.duration = librosa.get_duration(y=y, sr=sr)

    # Load the jams
    if not isinstance(jam, jams.JAMS):
        jam = jams.load(jam)

    data = dict()

    for op in ops:
        if isinstance(op, BaseTaskTransformer):
            data.update(op.transform(jam))
        elif isinstance(op, FeatureExtractor):
            data.update(op.transform(y, sr))
    return data


class Pump(object):
    '''Top-level pump object.

    This class is used to collect feature and task transformers

    Attributes
    ----------
    ops : list of (BaseTaskTransformer, FeatureExtractor)
        The operations to apply

    Examples
    --------
    Create a CQT and chord transformer

    >>> p_cqt = pumpp.feature.CQT('cqt', sr=44100, hop_length=1024)
    >>> p_chord = pumpp.task.ChordTagTransformer(sr=44100, hop_length=1024)
    >>> pump = pumpp.Pump(p_cqt, p_chord)
    >>> data = pump.transform('/my/audio/file.mp3', '/my/jams/annotation.jams')

    Access all the fields produced by this pump:

    >>> pump.fields
    {'chord/chord': Tensor(shape=(None, 170), dtype=<class 'bool'>),
     'cqt/mag': Tensor(shape=(None, 288), dtype=<class 'numpy.float32'>),
     'cqt/phase': Tensor(shape=(None, 288), dtype=<class 'numpy.float32'>)}

    Access a constituent operator by name:

    >>> pump['chord'].fields
    {'chord/chord': Tensor(shape=(None, 170), dtype=<class 'bool'>)}

    See Also
    --------
    transform
    '''

    def __init__(self, *ops):

        self.ops = []
        self.opmap = dict()
        for op in ops:
            self.add(op)

    def add(self, op):
        '''Add an operation to this pump.

        Parameters
        ----------
        op : BaseTaskTransformer, FeatureExtractor
            The operation to add

        Raises
        ------
        ParameterError
            if `op` is not of a correct type
        '''
        if not isinstance(op, (BaseTaskTransformer, FeatureExtractor)):
            raise ParameterError('op={} must be one of '
                                 '(BaseTaskTransformer, FeatureExtractor)'
                                 .format(op))

        if op.name in self.opmap:
            raise ParameterError('Duplicate operator name detected: {}'.format(op))

        self.opmap[op.name] = op
        self.ops.append(op)

    def transform(self, audio_f, jam=None):
        '''Apply the transformations to an audio file, and optionally JAMS object.

        Parameters
        ----------
        audio_f : str
            Path to audio file

        jam : optional, `jams.JAMS`, str or file-like
            Optional JAMS object/path to JAMS file/open file descriptor.

            If provided, this will provide data for task transformers.

        Returns
        -------
        data : dict
            Data dictionary containing the transformed audio (and annotations)
        '''

        return transform(audio_f, jam, *self.ops)

    def sampler(self, n_samples, duration, random_state=None):
        '''Construct a sampler object for this pump's operators.

        Parameters
        ----------
        n_samples : None or int > 0
            The number of samples to generate

        duration : int > 0
            The duration (in frames) of each sample patch

        random_state : None, int, or np.random.RandomState
            If int, random_state is the seed used by the random number
            generator;

            If RandomState instance, random_state is the random number
            generator;

            If None, the random number generator is the RandomState instance
            used by np.random.

        Returns
        -------
        sampler : pumpp.Sampler
            The sampler object

        See Also
        --------
        pumpp.sampler.Sampler
        '''

        return Sampler(n_samples, duration,
                       random_state=random_state,
                       *self.ops)

    @property
    def fields(self):
        out = dict()
        for op in self.ops:
            out.update(**op.fields)

        return out

    def layers(self):
        '''Construct Keras input layers for all feature transformers
        in the pump.

        Returns
        -------
        layers : {field: keras.layers.Input}
            A dictionary of keras input layers, keyed by the corresponding
            fields.
        '''

        L = dict()
        for op in self.ops:
            if hasattr(op, 'layers'):
                L.update(op.layers())
        return L

    def __getitem__(self, key):
        return self.opmap.get(key)
