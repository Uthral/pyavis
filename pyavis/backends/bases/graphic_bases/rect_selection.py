from typing import Tuple
from pyavis.shared.util.subject import Subject
from .graphic_element import GraphicElement

class RectSelection(GraphicElement):
    def __init__(
            self,
            position: Tuple[float, float],
            size: Tuple[float, float]
    ):
        GraphicElement.__init__(self, position)
        self._size = size
        self._handles = {}
        
        self.sizeChanged = Subject()

    @property
    def size(self):
        return self._size
    
    def set_size(self, size: Tuple[float, float], trigger = True):
        """
        Set the size of the of the rectangle.

        Parameters
        ----------
        size : Tuple[float, float]
            New width and height 
        trigger : bool, optional
            Trigger observer, by default True
        """
        old_size = self.size
        if old_size[0] == size[0] and old_size[1] == size[1]:
            return
        
        self._size = size
        self._abstract_set_size()

        if trigger:
            self.sizeChanged.emit(self, self.size, old_size)
    
    def add_handle(self, side: str, mirror: bool = False):
        '''
        Add or replace a handle that scales the rectangle.

        Parameters
        ----------
        side: 'left' | 'right' | 'top' | 'bottom'
            Side to add the handle to
        mirror:
            Mirror changes on the opposite side
        '''
        pass

    def remove_handle(self, side: str):
        '''
        Remove a handle from the rectangle.

        Parameters
        ----------
        side: 'left' | 'right' | 'top' | 'bottom'
            Side to remove the handle from
        '''
        pass

    def set_style(self, line_color, handle_color):
        '''
        Set the color of the selection lines and handels.

        Parameters
        ----------
        line_color : color.color | str, default: "default"
            Either "default" or values of the format 'color.color'
        handle_color : color.color | str, default: "default"
            Either "default" or values of the format 'color.color'
        '''
        if line_color == "default":
            from pyavis.config import get_style_config_value
            line_color = get_style_config_value("border_color")
        else:
            from pyavis.shared.util import color
            color._check_color(line_color)

        if handle_color == "default":
            from pyavis.config import get_style_config_value
            handle_color = get_style_config_value("fill_color")
        else:
            from pyavis.shared.util import color
            color._check_color(handle_color)
        
        self._abstract_set_style(line_color, handle_color)



    def _abstract_set_style(self, line_color, fill_color):
        pass

    def _abstract_set_size(self):
        pass