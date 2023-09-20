from abc import abstractmethod
from .widget import Widget


class BaseScrollArea(Widget):
    @abstractmethod
    def __init__(self, height: int):
        pass

    @abstractmethod
    def set_widget(widget: Widget):
        pass