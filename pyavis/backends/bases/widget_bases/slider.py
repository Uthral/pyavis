from abc import abstractmethod
from typing import Callable, Any
from .widget import Widget


class BaseIntSlider(Widget):
    
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

class BaseFloatSlider(Widget):
        
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