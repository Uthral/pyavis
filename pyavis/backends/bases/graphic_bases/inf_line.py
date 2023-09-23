
from typing import Any, Literal, Tuple

from pyavis.shared.util import Subject
from .graphic_element import GraphicElement

class InfLine(GraphicElement):
    def __init__(
            self,
            position: Tuple[float, float]=(1.0, 1.0),
            angle: float = 0.0
    ):
        '''
        Construct a new infinite line. 

        Parameters
        ----------
        position: (float, float)
            Position of the line
        angle: float
            Angle of the line in radians.
        '''
        GraphicElement.__init__(self, position)
        self.angleChanged = Subject()
        self._line_angle = angle

    @property
    def line_angle(self):
        return self._line_angle

    def set_angle(self, angle: float):
        '''
        Set the angle of the line.
        
        Parameters
        ----------
        angle: float
            New angle of the line in radians.
        '''
        old_line_angle = self._line_angle

        self.set_active_silent(angle)
        self.angleChanged.emit(self, self.line_angle, old_line_angle)

    def set_angle_silent(self, angle: float):
        '''
        Set the angle of the line.
        Does not trigger observers.
        
        Parameters
        ----------
        angle: float
            New angle of the line in radians.
        '''
        self._internal_set_angle(angle)
        self._abstract_set_angle()

    def _internal_set_angle(self, angle: float):
        self._line_angle = angle

    def _abstract_set_angle(self):
        pass

    def set_style(self, line_color: Any | Literal["default"]):
        '''
        Set the color of the infinite line.

        Parameters
        ----------
        line_color : color.color | str, default: "default"
            Either "default" or values of the format 'color.color'
        '''
        if line_color == "default":
            from pyavis.config import get_style_config_value
            line_color = get_style_config_value("line_color")
        else:
            from pyavis.shared.util import color
            color._check_color(line_color)
        
        self._abstract_set_style(line_color)

    def _abstract_set_style(self, line_color: Any):
        pass