

from typing import Tuple
from pyavis.shared.util.subject import Subject
from .graphic_element import GraphicElement


class Rectangle(GraphicElement):
    def __init__(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            width: float = 1.0,
            height: float = 1.0,
    ):
        GraphicElement.__init__(self, position)
        self.sizeChanged = Subject()

        self._width = width
        self._height = height

    @property
    def rect_size(self):
        return (self._width, self._height)

    @property
    def rect_width(self):
        return self._width
    
    @property
    def rect_height(self):
        return self._height
    
    def set_width(self, width: float):
        old_size = self.rect_size

        self.set_width_silent(width)
        self.sizeChanged.emit(self, self.rect_size, old_size)

    def set_width_silent(self, width: float):
        self._internal_set_width(width)
        self._abstract_set_width()

    def _internal_set_width(self, width: float):
        self._width = width

    def _abstract_set_width(self):
        pass

    def set_height(self, height: float):
        old_size = self.rect_size

        self.set_height_silent(height)
        self.sizeChanged.emit(self, self.rect_size, old_size)

    def set_height_silent(self, height: float):
        self._internal_set_height(height)
        self._abstract_set_height()

    def _internal_set_height(self, height: float):
        self._height = height
        
    def _abstract_set_height(self):
        pass

    def set_style(self, style: dict):
        pass