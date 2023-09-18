from copy import deepcopy

from pya import Astft, Asig
from pyavis.backends.bases.graphic_bases_v2 import Spectrogram

def spec_to_stft(spectrogram: Spectrogram, with_original_phase: bool = False) -> Astft:
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
    magnitude = spectrogram.get_spectrogram_data()
    stft = deepcopy(spectrogram.orig_spectrogram)

    print(spectrogram.orig_spectrogram.stft)

    stft.stft = magnitude * (spectrogram.orig_spectrogram.stft / np.abs(spectrogram.orig_spectrogram.stft))
    stft.stft = magnitude * (1.0 + 0.0j)
    stft.label = stft.label + '_edited'
    return stft

def spec_to_asig(spectrogram: Spectrogram, with_original_phase: bool = False, **kwargs) -> Asig:
    '''
    Return the displayed spectrogram as an :class:`Asig <pya.Asig>`.
    Assumes 'np.abs' as the display function.

    Parameters
    ----------
    spectrogram: Spectrogram
        Spectrogram to use
    with_orig_phase: bool
        If the phases of the original spectrogram shall be used, else a phase of 0 for all frequencies
    **kwargs:
        Keyword arguments for :func:`Astft.to_sig()`
    '''
    magnitude = spectrogram.get_spectrogram_data()
    stft = deepcopy(spectrogram.orig_spectrogram)

    stft.stft = magnitude * (spectrogram.orig_spectrogram.stft / np.abs(spectrogram.orig_spectrogram.stft))
    stft.stft = magnitude * (1.0 + 0.0j)
    stft.label = stft.label + '_edited'
    return stft.to_sig(**kwargs)