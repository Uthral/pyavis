


from typing import Literal

from overrides import override
from pyavis.backends.bases.graphic_bases_v2.track import Track

from matplotlib.axes import Axes
from matplotlib.figure import Figure

class TrackIPY(Track):
    def __init__(self, label: str, ax=None, fig=None):
        Track.__init__(self, label)

        self.ax: Axes = None
        self.fig: Figure = None
        if (ax is None and fig is None) or (ax is not None and fig is not None):
            raise Exception("Either figure or axis.")
        
        if ax is not None:
            self.ax: Axes = ax
        
        if fig is not None:
            self.fig: Figure = fig
            self.ax: Axes = self.fig.add_subplot()


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
    def _link_track(self, track: Track, axis: Literal['x', 'y']):
        if axis == 'x':
            if track is None:
                self.ax._shared_axes[axis].remove(self.ax)
            else:
                self.ax.sharex(track.ax)
        else:
            if track is None:
                self.ax._shared_axes[axis].remove(self.ax)
            else:
                self.ax.sharex(track.ax)

    def set_axis(self, axis):
        pass