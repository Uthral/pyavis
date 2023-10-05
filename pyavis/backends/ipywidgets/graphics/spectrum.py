from typing import Callable, Tuple

from pya import Asig, Aspec
from pyavis.backends.bases.graphic_bases.spectrum import Spectrum

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

import numpy as np

class SpectrumIPY(Spectrum):
    def __init__(        
        self,
        data: Asig | Aspec,
        position: Tuple[float, float] = (0.0, 0.0),
        scale: float = 1.0, 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
        **kwargs
    ):
        if 'ax' not in kwargs:
            raise KeyError("Axes not provided. Cannot instantiate SignalIPY.")

        Spectrum.__init__(self, data, position, scale, disp_func)
        self._ax: Axes = kwargs['ax']
        self._lines, = self._ax.plot(
            self.orig_spec.freqs + self.position[0],
            self.disp_func(self.orig_spec.rfftspec) * self.scale + self.position[1]
        )
        self.set_style("default")
    
    def remove(self):
        self._lines.remove()
        self._lines = None
        self._ax = None
    
    def _update_plot(self):
        self._lines.set_data((
            self.orig_spec.freqs + self.position[0],
            self.disp_func(self.orig_spec.rfftspec) * self.scale + self.position[1]
        ))
    
    def _abstract_set_active(self):
        self._lines.set_visible(self.active)
        self._lines.axes.figure.canvas.draw_idle()
    
    def _abstract_set_data(self):
        self._update_plot()
    
    def _abstract_set_position(self):
        self._update_plot()
    
    def _abstract_set_scale(self):
        self._update_plot()
    
    def _abstract_set_style(self, line_color):
        from pyavis.shared.util import color
        line_color = color._convert_color(line_color)
        self._lines.set_color(line_color)