from abc import abstractmethod
from .widget import Widget


class BaseScrollArea(Widget):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set_widget(widget: Widget):
        pass