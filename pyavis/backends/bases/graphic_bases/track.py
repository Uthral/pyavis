from abc import ABC, abstractmethod
from typing import Literal, Tuple
import numpy as np

from .axis import Axis
from .graphic_element import GraphicElement
from .rectangle import Rectangle
from .selection import Selection
from .signal import Signal


class Track(ABC):
    @abstractmethod
    def add_signal(self, position: Tuple[float, float], data: np.ndarray) -> Signal:
        pass

    @abstractmethod
    def add_rectangle(self, position: Tuple[float, float], size: Tuple[float, float]) -> Rectangle:
        pass

    @abstractmethod
    def remove(self, element: GraphicElement):
        pass

    def set_selection(self, selection: Selection):
        pass

    def get_selection(self) -> Selection | None:
        pass

    def unset_selection(self):
        pass


    @abstractmethod
    def set_style(self, **kwargs):
        pass

    @abstractmethod
    def allow_dragging(self, along_x: bool, along_y: bool):
        pass

    @abstractmethod
    def set_dragging_limits(self, x_limits: Tuple[int | None, int | None], y_limits: Tuple[float | None, float | None]):
        pass

    @abstractmethod
    def link_track(self, track: 'Track', axis: Literal["x", "y"]):
        pass

    @abstractmethod
    def set_axis(self, axis: Axis):
        pass