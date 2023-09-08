from abc import ABC, abstractmethod
from typing import List, Literal
from .axis import Axis

class Track(ABC):
    def __init__(self, label: str):
        self._label = label
        self._axis: List[Axis] = []

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


    