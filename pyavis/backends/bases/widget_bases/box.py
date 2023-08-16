from abc import abstractmethod
from .widget import Widget


class BaseVBox(Widget):

    @abstractmethod
    def add_widget(self, widget: Widget):
        pass

    @abstractmethod
    def remove_widget(self, widget: Widget):
        pass

class BaseHBox(Widget):

    @abstractmethod
    def add_widget(self, widget: Widget):
        pass

    @abstractmethod
    def remove_widget(self, widget: Widget):
        pass