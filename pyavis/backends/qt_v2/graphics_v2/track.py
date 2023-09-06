from typing import List, Literal, Tuple
from overrides import override

from pyqtgraph.Qt import QtCore, QtWidgets
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg

from pyavis.backends.bases.graphic_bases_v2.track import Track


class M_TrackQt(type(Track), type(pg.PlotItem)): pass
class TrackQt(Track, pg.PlotItem, metaclass=M_TrackQt):

    def __init__(self, label: str):
        pg.PlotItem.__init__(self)
        self.label = label

        self.setLabel('top', label)

    def add_signal(self) -> None:
        pass

    def add_line(self) -> None:
        pass

    def add_rect(self) -> None:
        pass

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

    def set_axis(self, axis):
        pass
