from abc import ABC

from pyavis.shared.util import Subject


class GraphicElement(ABC):
    def __init__(self):
        self.positionChanged = Subject()
        self.activeStateChanged = Subject()

        self.click = Subject()

        self.draggingBegin = Subject()
        self.dragging = Subject()
        self.draggingFinish = Subject()

        self.position = (0.0, 0.0)
        self.draggable = False
        self.clickable = False

    def set_position(self, x: int | float, y: int | float):
        '''
        Set position of graphic element.

        Parameters
        ----------
        x : float
            New x-position of element
        y : float
            New y-position of element
        '''
        if self.position[0] == x and self.position[1] == y:
            return
        
        old_pos = self.position
        new_pos = (x, y)

        self.position = new_pos
        self.positionChanged.emit(self, new_pos, old_pos)
    
    def set_active(self, active: bool = False):
        '''
        Hide / Show element.

        Parameters
        ----------
        active : bool, default: False
            Hide or show element
        '''
        if self.active == active:
            return

        old = self.active
        new = active

        self.active = new
        self.activeStateChanged.emit(self, new, old)