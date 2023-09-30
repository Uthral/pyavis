
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.transforms import Affine2D
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np
from typing import Callable, Tuple
from pya import Asig, Astft
from pyavis.backends.bases.graphic_bases.spectrogram import Spectrogram

import warnings

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
        self.with_bar = with_bar
        self._c_bar = None
        self._c_bar_ax = None

        self._init_mesh()

    def _init_mesh(self):
        self._spec = self._ax.pcolormesh(
            self.orig_spectrogram.times,
            self.orig_spectrogram.freqs,
            self.disp_func(self.orig_spectrogram.stft))
        
        self._abstract_set_position()
        self.toggle_color_bar(self.with_bar)
     
    def toggle_color_bar(self, show: bool):
        self.with_bar = show

        if self.with_bar and self._c_bar_ax is None:
            divider = make_axes_locatable(self._ax)
            self._c_bar_ax = divider.append_axes('right', size="2%", pad=0.03)
            self._c_bar = plt.colorbar(self._spec, cax=self._c_bar_ax)
        elif not self.with_bar and self._c_bar is not None:
            self._c_bar_ax.remove()
            self._c_bar_ax = None
            self._c_bar = None

        self._ax.figure.canvas.draw()

    def get_spectrogram_data(self):
        return self.disp_func(self.orig_spectrogram.stft)

    def clear_brush(self):
        warnings.warn("'clear_brush' not implemented for ipywidget backend.")
    
    def set_brush(self, brush_data=None, brush_mask=None, brush_center=..., draw_mode="set"):
        warnings.warn("'set_brush' not implemented for ipywidget backend.")

    def draw(self, freq: float, time: float):
        warnings.warn("'draw' not implemented for ipywidget backend.")

    def remove(self):
        if self._c_bar_ax is not None:
            self._c_bar_ax.remove()
            self._c_bar_ax = None
            self._c_bar = None
        self._spec.remove()
        self._spec = None
        self._ax = None

    def _abstract_set_data(self):
        self._spec.remove()
        self._spec = None

        if self._c_bar_ax is not None:
            self._c_bar_ax.remove()
            self._c_bar_ax = None
            self._c_bar = None
        
        self._init_mesh()

    def _abstract_set_active(self):
        self._spec.set_visible(self.active)
    
    def _abstract_set_position(self):
        translation = Affine2D().translate(*self.position)
        self._spec.set_transform(translation + self._spec.get_transform())

    def _abstract_set_scale(self):
        scale = Affine2D().scale(*self.scale)
        return super()._abstract_set_scale(scale + self._spec.get_transform())

    def set_style(self):
        pass