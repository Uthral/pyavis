from abc import ABC, abstractmethod
from typing import Tuple

from pyavis.shared.util import Subject


class GraphicElement(ABC):
    def __init__(
            self,
            position: Tuple[int | float, int | float] = (0.0, 0.0),
            active = True
    ):
        self.position = None
        self.active = None

        self._internal_set_position(*position)
        self._interal_set_active(active)

        self.positionChanged = Subject()
        self.activeStateChanged = Subject()

        self.onClick = Subject()
        self.onDraggingBegin = Subject()
        self.onDragging = Subject()
        self.onDraggingFinish = Subject()

        self._draggable = False
        self._clickable = False


    @property
    def clickable(self):
        return self._clickable
    
    @clickable.setter
    def clickable(self, value: bool):
        self._clickable = value

    @property
    def draggable(self):
        return self._draggable
    
    @draggable.setter
    def draggable(self, value: bool):
        self._draggable = value

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
        old_position = self.position
        if old_position[0] == x and old_position[1] == y:
            return
        
        self.set_position_silent(x, y)
        self.positionChanged.emit(self, self.position, old_position)

    def set_position_silent(self, x: int | float, y: int | float):
        '''
        Set position of graphic element.
        Does not trigger observers.

        Parameters
        ----------
        x : float
            New x-position of element
        y : float
            New y-position of element
        '''
        self._internal_set_position(x, y)
        self._abstract_set_position(self)

    def _internal_set_position(self, x: int | float, y: int | float):
        self.position = (x, y)

    def _abstract_set_position(self):
        pass

    def set_active(self, active = True):
        '''
        Hide / Show element.

        Parameters
        ----------
        active : bool, default: False
            Hide or show element
        '''
        old_active_state = self.active
        if old_active_state == active:
            return

        self.set_active_silent(active)
        self.activeStateChanged.emit(self, self.active, old_active_state)

    def set_active_silent(self, active = True):
        '''
        Hide / Show element.
        Does not trigger observers.

        Parameters
        ----------
        active : bool, default: False
            Hide or show element
        '''
        self._interal_set_active(self, active)
        self._abstract_set_active(self)

    def _interal_set_active(self, active = True):
        self.active = active

    def _abstract_set_active(self):
        pass