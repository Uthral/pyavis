
from typing import Callable

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from overrides import override
from pyavis.backends.bases.deprecated.base_classes import BaseSpectrogram
from pya import Asig, Astft

import numpy as np

class SpectrogramIPY(BaseSpectrogram):
    def __init__(self, x: Asig | Astft, disp_func: Callable[[np.ndarray], np.ndarray] = np.abs, fig_kw: dict = {}, spec_kw: dict = {}):
        self.fig_kw = fig_kw
        self.spec_kw = spec_kw

        if type(x) == Asig:
            self.orig_signal = x
            self.orig_spectrogram = x.to_stft()
        elif type(x) == Astft:
            self.orig_signal = None
            self.orig_spectrogram = x
        else:
            raise TypeError("Unknown data type x, x should be either Asig or Astft")
        self.disp_func = disp_func
        
        freqs = self.orig_spectrogram.freqs
        times = self.orig_spectrogram.times
        stft = self.orig_spectrogram.stft
        disp = disp_func(stft)

        self.figure = plt.figure(**self.fig_kw)
        self.spec = self.figure.add_subplot()
        mesh = self.spec.pcolormesh(times, freqs, disp, **self.spec_kw)

        show_bar = True
        if show_bar:
            divider = make_axes_locatable(self.spec)
            cax = divider.append_axes('right', size="2%", pad=0.03)
            _ = plt.colorbar(mesh, cax=cax)
    
    @override
    def get_native_widget(self):
        return self.figure.canvas

    @override
    def reset(self):
        '''
        Reset the image to the origninal :class:`Astft <pya.Astft>`
        '''
        freqs = self.orig_spectrogram.freqs
        times = self.orig_spectrogram.times
        stft = self.orig_spectrogram.stft
        disp = self.disp_func(stft)

        self.spec.clear()
        mesh = self.spec.pcolormesh(times, freqs, disp, **self.spec_kw)

        show_bar = True
        if show_bar:
            divider = make_axes_locatable(self.spec)
            cax = divider.append_axes('right', size="2%", pad=0.03)
            _ = plt.colorbar(mesh, cax=cax)


    @override
    def clear(self):
        '''
        Clear spectrogram
        '''
        self.spec.clear()


    @override
    def as_asig(self, **kwargs) -> Asig:
        '''
        Return the displayed STFT as an :class:`Asig <pya.Asig>`.

        Parameters
        ----------
        **kwargs :
            Keyword arguments for :func:`Astft.to_sig()`
        '''
        return self.orig_spectrogram.to_sig(**kwargs)

    @override
    def as_astft(self) -> Astft:
        '''
        Return the displayed STFT as an :class:`Astft <pya.Astft>`
        '''
        return self.orig_spectrogram

    @override
    def draw(self, freq: float, time: float):
        '''
        Draw at the time and position with the set brush.
        Does nothing if no brush data is set.

        Parameters
        ----------
        freq: float
            Frequencey to draw at
        time: float
            Time to draw at
        '''
        raise NotImplementedError()




