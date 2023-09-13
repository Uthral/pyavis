from typing import Tuple
from pyavis.shared.util.subject import Subject
from .graphic_element import GraphicElement

class RectSelection(GraphicElement):
    _handle_type = ["left", "right", "top", "bottom"]

    def __init__(self, position, size):
        GraphicElement.__init__(self, position, True)
        self._size = size
        self._handles = {}
        
        self.sizeChanged = Subject()

    @property
    def size(self):
        return self._size
    
    def set_size(self, size: Tuple[float, float]):
        '''
        Set the size of the of the rectangle.

        Parameters
        ----------
        size: (float, float)
            New width and height 
        '''
        self.set_size_silent(size)
        self.sizeChanged.emit(self, self.size)

    def set_size_silent(self, size: Tuple[float, float]):
        '''
        Set the size of the of the rectangle.
        Does not trigger observers.

        Parameters
        ----------
        size: (float, float)
            New width and height 
        '''
        self._internal_set_size(size)
        self._abstract_set_size()

    def _internal_set_size(self, size: Tuple[float, float]):
        '''
        Set the size of the of the rectangle.
        Only for internal usage.

        Parameters
        ----------
        size: (float, float)
            New width and height 
        '''
        self._size = size

    def _abstract_set_size(self):
        pass
        
    
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