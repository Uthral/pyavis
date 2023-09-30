

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
        self._size = (width, height)

    @property
    def rect_size(self):
        return self._size

    @property
    def rect_width(self):
        return self._size[0]
    
    @property
    def rect_height(self):
        return self._size[1]
    
    def set_size(self, size: Tuple[float, float], trigger = True):
        """
        Set the size of the rectangle.

        Parameters
        ----------
        size : Tuple[float, float]
            New size of the rectangle
        trigger : bool, optional
            Trigger observer, by default True
        """

        old_size = self.rect_size
        if old_size[0] == size[0] and old_size[1] == size[1]:
            return 
        
        self._size = size
        self._abstract_set_size()

        if trigger:
            self.sizeChanged.emit(self, self.rect_height, old_size)

    def set_style(self, border_color, fill_color):
        if border_color == "default":
            from pyavis.config import get_style_config_value
            border_color = get_style_config_value("border_color")
        else:
            from pyavis.shared.util import color
            color._check_color(border_color)

        if fill_color == "default":
            from pyavis.config import get_style_config_value
            fill_color = get_style_config_value("fill_color")
        else:
            from pyavis.shared.util import color
            color._check_color(fill_color)
        
        self._abstract_set_style(border_color, fill_color)


    def _abstract_set_size(self):
        pass

    def _abstract_set_style(self, border_color, fill_color):
        pass