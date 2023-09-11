
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.transforms import Affine2D
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np
from typing import Callable, Tuple
from pya import Asig, Astft
from pyavis.backends.bases.graphic_bases_v2.spectrogram import Spectrogram


class SpectrogramIPY(Spectrogram):
    def __init__(
        self,
        data: Asig | Astft,
        position: Tuple[float, float] = (0.0, 0.0), 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
        with_bar = True,
        **kwargs
    ):
        if 'ax' not in kwargs:
            raise KeyError("Axes not provided. Cannot instantiate SignalIPY.")

        Spectrogram.__init__(self, data, position, disp_func)
        self._ax: Axes = kwargs['ax']
        self.spec = self._ax.pcolormesh(
            self.orig_spectrogram.times,
            self.orig_spectrogram.freqs,
            self.disp_func(self.orig_spectrogram.stft))
        
        self.with_bar = with_bar
        self._c_bar = None
        self._c_bar_ax = None

        if with_bar:
            divider = make_axes_locatable(self._ax)
            self._c_bar_ax = divider.append_axes('right', size="2%", pad=0.03)
            self._c_bar = plt.colorbar(self.spec, cax=self._c_bar_ax)

        self.with_bar = with_bar
        

        self._abstract_set_position()

    def _abstract_set_active(self):
        self.spec.set_visible(self.active)
    
    def _abstract_set_position(self):
        translation = Affine2D().translate(*self.position)
        self.spec.set_transform(translation + self.spec.get_transform())
