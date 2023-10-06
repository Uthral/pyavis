from typing import Callable, Literal, Tuple

from pyavis.backends.bases.graphic_bases import GraphicElement, Track

import pyqtgraph as pg
from pyqtgraph.GraphicsScene.mouseEvents import *

from pya import Asig, Aspec, Astft
import numpy as np

from pyavis.backends.bases.graphic_bases.spectrum import Spectrum

from .axis import AxisQt
from .signal import SignalQt
from .rectangle import RectangleQt
from .infinite_line import InfLineQt
from .spectrogram import SpectrogramQt
from .rect_selection import RectSelectionQt
from .spectrum import SpectrumQt


class M_TrackQt(type(Track), type(pg.PlotItem)): pass
class TrackQt(Track, pg.PlotItem, metaclass=M_TrackQt):

    def __init__(self, label: str):
        Track.__init__(self, label)
        pg.PlotItem.__init__(self)

        self.setTitle(self._label)

        l_axis = AxisQt("left", self.getAxis("left"))
        b_axis = AxisQt("bottom", self.getAxis("bottom"))
        self._axis.append(l_axis)
        self._axis.append(b_axis)

        self.set_style('default')

    def add_signal(            
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            scale: float = 1.0,
            *args,
            **kwargs
    ) -> SignalQt:
        sig = SignalQt(position, scale, *args, **kwargs)
        self.addItem(sig)
        return sig

    def add_spectrum(
            self, 
            data: Asig | Aspec, 
            position: Tuple[float, float] = (0.0, 0.0), 
            scale: float = 1, 
            disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
    ) -> Spectrum:
        spec = SpectrumQt(data, position, scale, disp_func)
        self.addItem(spec)
        return spec

    def add_line(self, position, angle) -> InfLineQt:
        line = InfLineQt(position, angle)
        self.addItem(line)
        return line

    def add_rect(self, position, width, height) -> RectangleQt:
        rect = RectangleQt(position, width, height)
        self.addItem(rect)
        return rect

    def add_spectrogram(        
        self, 
        data: Asig | Astft,
        position: Tuple[float, float] = (0.0, 0.0), 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
        with_bar: bool = True,
        **kwargs
    ) -> SpectrogramQt:
        spec = SpectrogramQt(data=data, position=position, disp_func=disp_func, with_bar=with_bar, plt_item=self, **kwargs)
        self.addItem(spec)
        return spec

    def add_selection(self, pos, width, height) -> RectSelectionQt:
        sel = RectSelectionQt(pos, width, height)
        self.addItem(sel)
        return sel
    
    def remove(self, element: GraphicElement):
        if isinstance(element, SpectrogramQt):
            element.toggle_color_bar(False)
        self.removeItem(element)
    
    def _link_track(self, track: 'Track', axis: Literal["x", "y"]):
        if axis == 'x':
            self.getViewBox().setXLink(track.getViewBox() if track is not None else None)
        elif axis == 'y':
            self.getViewBox().setYLink(track.getViewBox() if track is not None else None)
        else:
            raise ValueError("Not a valid axis")





    def set_axis(self, side: Literal['top', 'bottom', 'left', 'right'], spacing, disp_func):
        axis = self.get_axis(side)

        if axis is not None:
            axis.set_disp_func(disp_func)
            axis.tick_spacing(spacing)
            axis.toggle_visibility()
            return
        
        axis = pg.AxisItem(side)
        self.setAxisItems({side: axis})

        axis = AxisQt(side, axis)
        axis.set_disp_func(disp_func)
        axis.tick_spacing(spacing)
        axis.toggle_visibility()

        self._axis.append(axis)

        return axis
    
    def set_x_view_limits(self, x_start, x_end):
        self.getViewBox().setXRange(x_start, x_end)
        
    def set_y_view_limits(self, y_start, y_end):
        self.getViewBox().setYRange(y_start, y_end)

    def _abstract_set_style(self, background_color):
        from pyavis.shared.util import color
        background_color = color._convert_color(background_color)
        self.getViewBox().setBackgroundColor(background_color)