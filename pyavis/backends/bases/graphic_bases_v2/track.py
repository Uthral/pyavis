from abc import ABC, abstractmethod
from typing import List, Literal
from .axis import Axis

from .signal import Signal
from .rectangle import Rectangle
from .inf_line import InfLine
from .spectrogram import Spectrogram
from .rect_selection import RectSelection

class Track(ABC):
    def __init__(self, label: str):
        self._label = label
        self._axis: List[Axis] = []

    def add_signal(self) -> Signal:
        pass

    def add_line(self) -> InfLine:
        pass

    def add_rect(self) -> Rectangle:
        pass

    def add_spectrogram(self) -> Spectrogram:
        pass

    def add_selection(self) -> RectSelection:
        pass

    def set_style(self):
        pass
    
    def link_track(self, track: 'Track', axis: Literal["x", "y"]):
        if axis != 'x' and axis !='y':
            raise ValueError("Not a valid axis")
        
        self._link_track(track, axis)
    
    @abstractmethod
    def _link_track(self, track: 'Track', axis: Literal["x", "y"]):
        pass









    def get_axis(self, side: Literal['top', 'bottom', 'left', 'right']) -> Axis:
        v = [value for value in self._axis if value._side == side]
        return v[0] if len(v) > 0 else None
    
    def toggle_axis(self, side: Literal['top', 'bottom', 'left', 'right'], show=True):
        axis = self.get_axis(side)
        if axis is not None:
            axis.toggle_visibility(show)
        else:
            raise ValueError(f"Axis not set for side: {side}")
    
    def set_axis(self, side: Literal['top', 'bottom', 'left', 'right'], spacing, disp_func) -> Axis:
        pass


    