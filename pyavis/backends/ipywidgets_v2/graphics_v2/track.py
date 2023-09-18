


from typing import Literal

from overrides import override
from pyavis.backends.bases.graphic_bases_v2 import GraphicElement, Track

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .axis import AxisIPY
from .signal import SignalIPY
from .rectangle import RectangleIPY
from .inf_line import InfLineIPY
from .spectrogram import SpectrogramIPY

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
        
        l_axis = AxisIPY("left", self.ax.yaxis)
        b_axis = AxisIPY("bottom", self.ax.xaxis)

        self._axis.append(l_axis)
        self._axis.append(b_axis)


    def add_signal(self, position, size, *args, **kwargs) -> SignalIPY:
        sig = SignalIPY(position, size, *args, **kwargs, ax=self.ax)
        return sig

    def add_line(self, position, angle) -> InfLineIPY:
        line = InfLineIPY(position, angle, ax=self.ax)
        return line

    def add_rect(self, position, width, height) -> RectangleIPY:
        rect = RectangleIPY(position, width, height, ax=self.ax)
        return rect

    def add_spectrogram(self, data, position, disp_func, with_bar) -> SpectrogramIPY:
        spec = SpectrogramIPY(data, position, disp_func, with_bar, ax=self.ax)
        return spec

    def add_selection(self) -> None:
        raise NotImplementedError()
    
    def remove(self, element: GraphicElement):
        if isinstance(element, SpectrogramIPY):
            element.toggle_color_bar(False)
        element.remove()

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
                self.ax.sharey(track.ax)


    def set_axis(self, side: Literal['top', 'bottom', 'left', 'right'], spacing, disp_func) -> AxisIPY:
        axis = self.get_axis(side)

        if axis is not None:
            axis.set_disp_func(disp_func)
            axis.tick_spacing(spacing)
            axis.toggle_visibility(show=True)
            return

        if side == 'top':
            n_axes = self.ax.twinx()
            axis = n_axes.xaxis
        elif side == 'bottom':
            axis = self.ax.xaxis
        elif side == 'right':
            n_axes = self.ax.twiny()
            axis = n_axes.yaxis
        elif side == 'left':
            axis = self.ax.yaxis
        else:
            raise ValueError("Not a valid orientation.")
        
        axis = AxisIPY(side, axis)
        axis.set_disp_func(disp_func)
        axis.tick_spacing(spacing)
        axis.toggle_visibility(show=True)

        self._axis.append(axis)
    
        return axis
    
    def set_x_view_limits(self, x_start, x_end):
        self.ax.set_xlim((x_start, x_end))

    def set_y_view_limits(self, y_start, y_end):
        self.ax.set_ylim((y_start, y_end))