from abc import abstractmethod
from typing import Literal
from pyavis.shared.util import Subject
from .graphic_element import GraphicElement


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