"""
Abstract base classes that implement the shared functionality between
different backends.
"""
from abc import ABC, abstractmethod
from typing import Callable, List, Any, Tuple

class Widget(ABC):
    @abstractmethod
    def get_native_widget(self):
        pass

    @abstractmethod
    def show(self):
        pass

class BaseTrack(ABC):
    @abstractmethod
    def __init__(self, label: str, sampling_rate: int, **kwargs):
        pass

    @abstractmethod
    def add_signal(self, position: int, signal, **kwargs):
        pass

    @abstractmethod
    def remove_signal(self, signal):
        pass

    @abstractmethod
    def remove_at_position(self, position: int):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

class BaseSelection(ABC):
    @abstractmethod
    def __init__(self, indices: List[int], start: int, end: int, **kwargs):
        pass
    
    @abstractmethod
    def add_index(self, index: int):
        pass

    @abstractmethod
    def remove_index(self, index: int):
        pass

    @abstractmethod
    def update_region(self, region: Tuple[int, int]):
        pass
class AbstractMultiTrackVisualizer(Widget):
    @abstractmethod
    def add_selection(self, indices: List[int], start: int, end: int) -> BaseSelection:
        pass
    
    @abstractmethod
    def remove_selection(self, selection: BaseSelection):
        pass

    @abstractmethod
    def add_track(self, label: str, sampling_rate: int, **kwargs) -> BaseTrack:
        pass

    @abstractmethod
    def remove_track(self, identifier: int | str | BaseTrack):
        pass

    @abstractmethod
    def update_track_height(self, track_height: int):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

class AbstractSpectrogramVisualizer(Widget):
    pass

class AbstractButton(Widget):

    @abstractmethod
    def __init__(self, label: str):
        pass

    @abstractmethod
    def add_on_click(self, func: Callable):
        pass

    @abstractmethod
    def remove_on_click(self, func: Callable):
        pass

class AbstractVBox(Widget):

    @abstractmethod
    def add_widget(self, widget: Widget):
        pass

    @abstractmethod
    def remove_widget(self, widget: Widget):
        pass

class AbstractHBox(Widget):

    @abstractmethod
    def add_widget(self, widget: Widget):
        pass

    @abstractmethod
    def remove_widget(self, widget: Widget):
        pass

class AbstractIntSlider(Widget):
    
    @abstractmethod
    def __init__(self, description: str, orientation: str, default: int, min: int, max: int, step: int):
        pass

    @abstractmethod
    def set_value(self, value: int):
        pass

    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def add_on_value_changed(self, func: Callable[[Any], None]):
        pass

    @abstractmethod
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        pass

class AbstractFloatSlider(Widget):
        
    @abstractmethod
    def __init__(self, description: str, orientation: str, default: float, min: float, max: float, step: float):
        pass

    @abstractmethod
    def set_value(self, value: float):
        pass

    @abstractmethod
    def get_value(self) -> float:
        pass

    @abstractmethod
    def add_on_value_changed(self, func: Callable[[Any], None]):
        pass

    @abstractmethod
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        pass

class AbstractDropDown(Widget):

    @abstractmethod
    def __init__(self, description: str, options: List[Any], default: Any):
        pass

    @abstractmethod
    def get_value(self) -> Any | None:
        pass

    @abstractmethod
    def add_on_selection_changed(self, func: Callable[[Any], None]):
        pass

    @abstractmethod
    def remove_on_selection_changed(self, func: Callable[[Any], None]):
        pass

class AbstractToolBar(Widget):
    pass
