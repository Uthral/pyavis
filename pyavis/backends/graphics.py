


from abc import ABC, abstractmethod
from typing import Callable, Tuple, List, Literal

import numpy as np

from pyavis.shared.util import Subject

class GraphicElement(ABC):
    def __init__(self):
        self.positionChanged = Subject()
        self.activeStateChanged = Subject()

        self.position = (0.0, 0.0)
        self.draggable = False
        self.clickable = False

    def set_position(self, x: int | float, y: int | float):
        '''
        Set position of graphic element.

        Parameters
        ----------
        x : float
            New x-position of element
        y : float
            New y-position of element
        '''
        if self.position[0] == x and self.position[1] == y:
            return
        
        old_pos = self.position
        new_pos = (x, y)

        self.position = new_pos
        self.positionChanged.emit(self, new_pos, old_pos)
    
    def set_active(self, active: bool = False):
        '''
        Hide / Show element.

        Parameters
        ----------
        active : bool, default: False
            Hide or show element
        '''
        if self.active == active:
            return

        old = self.active
        new = active

        self.active = new
        self.activeStateChanged.emit(self, new, old)

class Rectangle(GraphicElement):
    def __init__(self):
        GraphicElement.__init__(self)
        self.sizeChanged = Subject()

    @abstractmethod
    def set_size(self, width: float, height: float):
        pass

    @abstractmethod
    def set_style(self, style: dict):
        pass

class Signal(GraphicElement):
    def __init__(self):
        GraphicElement.__init__(self)
        self.dataChanged = Subject()
        self.sizeChanged = Subject()

    @abstractmethod
    def set_data(self, data):
        pass
    
    @abstractmethod
    def set_size(self, size: float | Literal["auto"]):
        pass
    
    @abstractmethod
    def set_style(self, style: dict | Literal["default"]):
        pass

class Selection(ABC):
    def __init__(self, orientation: str, region: Tuple[float, float]):
        self.regionChanged = Subject()
        self._orientation = orientation
        self._region = region
        self._active = True

    def set_region(self, region: Tuple[float, float]):
        if self._region[0] == region[0] and self._region[1] == region[1]:
            return

        self._region = region
        self.regionChanged.emit(self, region)

    def get_region(self) -> Tuple[float, float]:
        return self._region

    def set_active(self, active: bool):
        self._active = active

    def set_style(self, style):
        pass


class Axis(ABC):
    @abstractmethod
    def set_disp_func(self, func: Callable[[float], str]):
        pass
    
    @abstractmethod
    def set_spacing(self, spacing: Tuple[float, float]=None):
        pass

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

    def get_selection(self) -> Selection:
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

class MultiTrack(ABC):
    def __init__(self):
        self.trackAdded = Subject()
        self.trackRemoved = Subject()
        self.tracks = []

    @abstractmethod
    def add_track(self, label: str, sampling_rate: int, **kwargs) -> Track:
        pass

    @abstractmethod
    def remove_track(self, identifier: int | str | Track):
        pass

    @abstractmethod
    def update_track_height(self, track_height: int):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass