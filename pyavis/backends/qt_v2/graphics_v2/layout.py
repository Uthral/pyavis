from overrides import override
from pyavis.backends.bases.graphic_bases_v2 import Layout

import pyqtgraph as pg

from pyavis.backends.qt_v2.graphics_v2.track import TrackQt

class M_LayoutQt(type(Layout), type(pg.GraphicsLayout)): pass
class LayoutQt(Layout, pg.GraphicsLayout, metaclass=M_LayoutQt):
    def __init__(self, rows: int = 1, columns: int = 1):
        Layout.__init__(self, rows, columns)
        pg.GraphicsLayout.__init__(self)

        for row in range(self.layout_rows):
            self.layout.setRowStretchFactor(row, 1)

        for column in range(self.layout_columns):
            self.layout.setColumnStretchFactor(column, 1)
    
    @override
    def remove_track(self, track):
        self.removeItem(track)
    
    @override
    def _add_track(self, label: str, row: int, column: int, rowspan: int = 1, colspan: int = 1) -> TrackQt:
        track = TrackQt(label)
        self.addItem(track, row, column, rowspan, colspan)
        return track

    
    # @override
    # def add_track(self, track, row, column, rowspan=1, colspan=1):
    #     if row > self._rows - 1 or column > self._columns - 1:
    #         raise Exception("Exceeding size of layout.")
        
    #     self.addItem(track, row=row, col=column, rowspan=rowspan, colspan=colspan)

    # @override
    # def remove_track(self, track):
    #     self.removeItem(track)
    #     self._set_column_stretch()

    # def _set_column_stretch(self):
    #     for row in range(self._rows):
    #         self.layout.setRowStretchFactor(row, 1)

    #     for column in range(self._columns):
    #         self.layout.setColumnStretchFactor(column, 1)