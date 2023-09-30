from abc import ABC, abstractmethod
from typing import Tuple

from pyavis.shared.util import Subject


class GraphicElement(ABC):

    def __init__(
            self,
            position: Tuple[int | float, int | float] = (0.0, 0.0),
            active = True
    ):
        self.position = position
        self.active = active

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

    def set_position(self, x: int | float, y: int | float, trigger = True):
        """
        Set the position of the element.

        Parameters
        ----------
        x : int | float
            New x-position of the element
        y : int | float
            New y-position of the element
        trigger : bool, optional
            Trigger observer, by default True
        """
        old_position = self.position
        if old_position[0] == x and old_position[1] == y:
            return
        
        self.position = (x, y)
        self._abstract_set_position()
        
        if trigger:
            self.positionChanged.emit(self, self.position, old_position)

    def set_active(self, active = True, trigger = True):
        """
        Hide or show the element.

        Parameters
        ----------
        active : bool, optional
            Change active state to hide or show element, by default True
        trigger : bool, optional
            Trigger observer, by default True
        """
        old_active_state = self.active
        if old_active_state == active:
            return
        
        self.active = active
        self._abstract_set_active()

        if trigger:
            self.activeStateChanged.emit(self, self.active, old_active_state)

    def _abstract_set_position(self):
        pass

    def _abstract_set_active(self):
        pass