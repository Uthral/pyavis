from abc import abstractmethod
from typing import Callable
from .widget import Widget


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