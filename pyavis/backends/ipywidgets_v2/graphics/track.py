
from typing import Literal, Tuple
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from overrides import override
from pyavis.backends.bases.graphic_bases import GraphicElement, Track, Axis

class M_TrackIPY(type(Track), type(Axes)): pass
class TrackIPY(Track):
    def __init__(self):
        self.fig = None
        self.ax: Axes = None
        self.elements = []
        self.execute_queue = []

    def set_ax(self, ax: Axes):
        self.ax = ax
        for element in self.elements:
            element.set_ax(ax)

    def react_to_ax(self):
        if self.ax is None:
            return
        
        for exec in self.execute_queue:
            exec()
        exec = []

    def link_track(self, track: 'Track', axis: Literal["x", "y"]):
        if axis != 'x' and axis !='y':
            raise ValueError("Not a valid axis")

        if self.ax is None:
            self.execute_queue.append(lambda track=track, axis=axis: self._link_track(track, axis))
        else:
            self._link_track(track, axis)
    
    def _link_track(self, track: 'Track', axis: Literal["x", "y"]):
        if axis == 'x':
            if track is None:
                self.ax._shared_axes['x'].remove(self.ax)
            else:
                self.ax.sharex(track.ax)
        else:
            if track is None:
                self.ax._shared_axes['y'].remove(self.ax)
            else:
                self.ax.sharex(track.ax)


    def add(self, element: GraphicElement):
        raise NotImplementedError()

    def remove(self, element: GraphicElement):
        raise NotImplementedError()

    def set_axis(self, axis: Axis):
        raise NotImplementedError()

    def set_style(self, **kwargs):
        raise NotImplementedError()

    def allow_dragging(self, along_x: bool, along_y: bool):
        raise NotImplementedError()

    def set_dragging_limits(self, x_limits: Tuple[int | None, int | None], y_limits: Tuple[float | None, float | None]):
        raise NotImplementedError()

