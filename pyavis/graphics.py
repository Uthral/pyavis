


from abc import ABC, abstractmethod
from typing import Tuple

import numpy as np


class Signal(ABC):
    @abstractmethod
    def set_data(self, data):
        pass
    
    @abstractmethod
    def set_signal_size(self, size: float | str):
        pass

    @abstractmethod
    def set_rectangle_size(self, size: float | str):
        pass
    
    @abstractmethod
    def update_position(self, position: Tuple[int, float]):
        pass
    
    @abstractmethod
    def set_style(self, signal_style: dict | str, rect_style: dict | str):
        pass

    @abstractmethod
    def toggle_rectangle(self, show_rect: bool = False):
        pass

class Track(ABC):

    @abstractmethod
    def add_signal(self, position: Tuple[float, float], data: np.ndarray) -> Signal:
        pass

    @abstractmethod
    def remove_signal(self, signal):
        pass

    @abstractmethod
    def set_style(self, **kwargs):
        pass

    @abstractmethod
    def allow_signal_dragging(self, along_x: bool, along_y: bool):
        pass

    @abstractmethod
    def set_dragging_limits(self, x_limits: Tuple[int, int], y_limits: Tuple[float, float]):
        pass

    @abstractmethod
    def set_axis(self, axis):
        pass