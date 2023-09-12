from overrides import override
from pyavis.backends.bases.graphic_bases import Layout

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

from pyavis.backends.bases.graphic_bases import Track
from .track import TrackIPY

class LayoutIPY(Layout):
    def __init__(self, rows: int = 1, columns: int = 1):
        Layout.__init__(self, rows, columns)

        self.fig: Figure = None
        self.grid: GridSpec = self.fig.add_gridspec(rows, columns)

        self.tracks = []

    @override
    def add_track(self, track: Track, row: int, column: int, rowspan: int = 1, colspan: int = 1) -> TrackIPY:
        row_start, row_end = row, row + rowspan
        column_start, column_end = column, column + colspan

        self.tracks.append(track)
        if self.fig is not None:
            ax = self.fig.add_subplot(self.grid[row_start:row_end, column_start:column_end])
            track.set_ax(ax)

        self.tracks.append(track)

        return track

    @override
    def remove_track(self, track):
        if self.fig is not None:
            self.fig.delaxes(track)

    def set_figure(self):
        pass
