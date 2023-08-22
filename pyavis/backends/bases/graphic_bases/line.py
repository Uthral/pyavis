from abc import abstractmethod

from pyavis.backends.bases.graphic_bases import GraphicElement
from pyavis.shared.util import Subject

class Line(GraphicElement):
    def __init__(self, pos, angle):
        GraphicElement.__init__(self)
        self.angleChanged = Subject()

        super().set_position(pos[0], pos[1])
        self._line_angle = angle
    
    @property
    @abstractmethod
    def line_angle(self):
        return self._line_angle
    
    @line_angle.setter
    @abstractmethod
    def line_angle(self, angle):
        self._line_angle = angle   

    @abstractmethod
    def set_style(self, style):
        pass
