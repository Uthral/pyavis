from copy import deepcopy

from pya import Astft, Asig
from pyavis.backends.bases.graphic_bases import Spectrogram

import numpy as np

def spec_to_stft(spectrogram: Spectrogram, inverted_display_func = None, with_original_phase: bool = False) -> Astft:
    '''
    Return the displayed spectrogram as an :class:`Astft <pya.Astft>`.
    Assumes 'np.abs' as the display function.

    Parameters
    ----------
    spectrogram: Spectrogram
        Spectrogram to use
    with_original_phase: bool
        If the phases of the original spectrogram shall be used, else a phase of 0 for all frequencies
    '''
    if inverted_display_func is not None:
        magnitude = inverted_display_func(spectrogram.get_spectrogram_data())
    else:
        magnitude = spectrogram.get_spectrogram_data()
    stft = deepcopy(spectrogram.orig_spectrogram)

    if with_original_phase:
        stft.stft = magnitude * (spectrogram.orig_spectrogram.stft / np.abs(spectrogram.orig_spectrogram.stft))
    else:
        stft.stft = magnitude * (1.0 + 0.0j)

    stft.label = stft.label + '_edited'
    return stft

def spec_to_asig(spectrogram: Spectrogram, inverted_display_func = None, with_original_phase: bool = False, **kwargs) -> Asig:
    '''
    Return the displayed spectrogram as an :class:`Asig <pya.Asig>`.
    Assumes 'np.abs' as the display function.

    Parameters
    ----------
    spectrogram: Spectrogram
        Spectrogram to use
    inverted_display_func: (np.ndarray) -> np.ndarray
        If not np.abs
    with_orig_phase: bool
        If the phases of the original spectrogram shall be used, else a phase of 0 for all frequencies
    **kwargs:
        Keyword arguments for :func:`Astft.to_sig()`
    '''
    if inverted_display_func is not None:
        magnitude = inverted_display_func(spectrogram.get_spectrogram_data())
    else:
        magnitude = spectrogram.get_spectrogram_data()

    stft = deepcopy(spectrogram.orig_spectrogram)

    if with_original_phase:
        stft.stft = magnitude * (spectrogram.orig_spectrogram.stft / np.abs(spectrogram.orig_spectrogram.stft))
    else:
        stft.stft = magnitude * (1.0 + 0.0j)

    stft.label = stft.label + '_edited'
    return stft.to_sig(**kwargs)