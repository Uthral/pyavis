from abc import abstractmethod
from .widget import Widget
from ..graphic_bases import Layout

class BaseGraphicDisp(Widget):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def set_displayed_item(self, item: Layout):
        pass