from typing import List, Literal, Tuple
from overrides import override

from pyqtgraph.Qt import QtCore, QtWidgets
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg

from pyavis.backends.bases.graphic_bases_v2.track import Track


from .axis import AxisQt
from .signal import SignalQt
from .rectangle import RectangleQt
from .inf_line import InfLineQt


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

    def add_signal(self, position, size, *args, **kwargs) -> SignalQt:
        sig = SignalQt(position, size, *args, **kwargs)
        self.addItem(sig)
        return sig

    def add_line(self, position, angle) -> InfLineQt:
        line = InfLineQt(position, angle)
        self.addItem(line)
        return line

    def add_rect(self, position, width, height) -> RectangleQt:
        rect = RectangleQt(position, width, height)
        self.addItem(rect)
        return rect

    def add_spectrogram(self) -> None:
        pass

    def add_selection(self) -> None:
        pass

    def set_style(self):
        pass
    
    @override
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
