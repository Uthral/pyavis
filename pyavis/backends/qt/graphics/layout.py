from pyavis.backends.bases.graphic_bases import Layout
from pyavis.backends.qt.graphics.track import TrackQt

import pyqtgraph as pg


class M_LayoutQt(type(Layout), type(pg.GraphicsLayout)): pass
class LayoutQt(Layout, pg.GraphicsLayout, metaclass=M_LayoutQt):
    def __init__(self, rows: int = 1, columns: int = 1):
        Layout.__init__(self, rows, columns)
        pg.GraphicsLayout.__init__(self)

        for row in range(self.layout_rows):
            self.layout.setRowStretchFactor(row, 1)

        for column in range(self.layout_columns):
            self.layout.setColumnStretchFactor(column, 1)

        self.set_style("default")
    
    def remove_track(self, track):
        self.removeItem(track)
    
    def _add_track(self, label: str, row: int, column: int, rowspan: int = 1, colspan: int = 1) -> TrackQt:
        track = TrackQt(label)
        self.addItem(track, row, column, rowspan, colspan)
        return track
    
    def _abstract_set_style(self, background_color):
        from pyavis.shared.util import color
        background_color = color._convert_color(background_color)
        v = self.getViewBox()

        if isinstance(v, pg.ViewBox):
            v.setBackgroundColor(background_color)
        elif isinstance(v, pg.GraphicsView):
            v.setBackground(background_color)
