from abc import abstractmethod
from typing import Callable, Any
from .widget import Widget

from pyavis.shared.util.subject import Subject

class BaseButton(Widget):

    @abstractmethod
    def __init__(self, label: str):
        pass

    @abstractmethod
    def add_on_click(self, func: Callable):
        pass

    @abstractmethod
    def remove_on_click(self, func: Callable):
        pass

class BaseToggleButton(Widget):

    @abstractmethod
    def __init__(self, label: str, icon: Any = None, default_toggle_state: bool = False):
        pass

    @abstractmethod
    def add_on_toggle(self, func: Callable):
        pass

    @abstractmethod
    def remove_on_toggle(self, func: Callable):
        pass