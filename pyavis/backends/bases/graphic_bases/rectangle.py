from abc import abstractmethod
from pyavis.backends.bases.graphic_bases.graphic_element import GraphicElement
from pyavis.shared.util import Subject


class Rectangle(GraphicElement):
    def __init__(self):
        GraphicElement.__init__(self)
        self.sizeChanged = Subject()

    @abstractmethod
    def set_size(self, width: float, height: float):
        pass

    @abstractmethod
    def set_style(self, style: dict):
        pass