from overrides import override


import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

from pyavis.backends.bases.graphic_bases_v2 import Layout
from .track import TrackIPY

class LayoutIPY(Layout):
    def __init__(self, rows: int = 1, columns: int = 1):
        Layout.__init__(self, rows, columns)

        self.fig: Figure = plt.figure()
        self.grid: GridSpec = self.fig.add_gridspec(rows, columns)

        self.set_style('default')
    
    @override
    def remove_track(self, track):
        if track.ax.fig == self.fig:
            track.ax.remove()

        self.fig.canvas.draw_idle()

    @override
    def _add_track(self, label: str, row: int, column: int, rowspan: int = 1, colspan: int = 1, *args, **kwargs) -> TrackIPY:
        row_start, row_end = row, row + rowspan
        col_start, col_end = column, column + colspan

        ax = self.fig.add_subplot(self.grid[row_start:row_end, col_start:col_end])

        ax.set_title(label)
        track = TrackIPY(label, ax=ax)
        return track
    
    def _abstract_set_style(self, background_color):
        from pyavis.shared.util import color
        background_color = color._convert_color(background_color)
        self.fig.set_facecolor(background_color)