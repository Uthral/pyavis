"""
Abstract base classes that implement the shared functionality between
different backends.
"""
from abc import ABC, abstractmethod
from typing import Callable

class Widget(ABC):
    @abstractmethod
    def get_native_widget(self):
        pass

    # @abstractmethod
    # def show(self):
    #     pass

class AbstractMultiTrackVisualizer(Widget):
    pass

class AbstractButton(Widget):

    @abstractmethod
    def __init__(self, label: str, onClick: Callable):
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

class AbstractSlider(Widget):
    pass

class AbstractSelect(Widget):
    pass

class AbstractRangeSlider(Widget):
    pass