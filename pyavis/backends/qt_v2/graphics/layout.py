from abc import abstractmethod
from overrides import override
from pyavis.backends.bases.graphic_bases import Layout
from .track import TrackQt

import pyqtgraph as pg

class M_LayoutQt(type(Layout), type(pg.GraphicsLayout)): pass
class LayoutQt(Layout, pg.GraphicsLayout, metaclass=M_LayoutQt):
    def __init__(self, rows: int = 1, columns: int = 1):
        Layout.__init__(self, rows, columns)
        pg.GraphicsLayout.__init__(self)

        self._set_column_stretch()
    
    @override
    def add_track(self, track, row, column, rowspan=1, colspan=1):
        if row > self._rows - 1 or column > self._columns - 1:
            raise Exception("Exceeding size of layout.")
        
        self.addItem(track, row=row, col=column, rowspan=rowspan, colspan=colspan)

    @override
    def remove_track(self, track):
        self.removeItem(track)
        self._set_column_stretch()

    def _set_column_stretch(self):
        for row in range(self._rows):
            self.layout.setRowStretchFactor(row, 1)

        for column in range(self._columns):
            self.layout.setColumnStretchFactor(column, 1)