
from typing import Any, Literal, Tuple

from pyavis.shared.util import Subject
from .graphic_element import GraphicElement

class InfiniteLine(GraphicElement):
    """_summary_
    Base class representing an infinite line.
    """
    def __init__(
            self,
            position: Tuple[float, float]=(0.0, 0.0),
            angle: float = 0.0
    ):
        """
        Construct a new infinite line.

        Parameters
        ----------
        position : Tuple[float, float], optional
            Position of the line, by default (0.0, 0.0)
        angle : float, optional
            Angle of the line in radians, by default 0.0
        """
        GraphicElement.__init__(self, position)
        self.angleChanged = Subject()
        self._line_angle = angle

    @property
    def line_angle(self):
        return self._line_angle

    def set_line_angle(self, angle: float, trigger = True):
        """
        Set the angle of the line.

        Parameters
        ----------
        angle : float
            New angle of the line, in radians.
        trigger : bool, optional
            Trigger observer, by default True
        """
        old_line_angle = self._line_angle
        if old_line_angle == angle:
            return
        
        self._line_angle = angle
        self._abstract_set_line_angle()

        if trigger:
            self.angleChanged.emit(self, self.line_angle, old_line_angle)

    def set_style(self, line_color: Any | Literal["default"]):
        """
        Set the color of the infinite line.

        Parameters
        ----------
        background_color : color | "default"
            Either "default" or color values
        """
        if line_color == "default":
            from pyavis.config import get_style_config_value
            line_color = get_style_config_value("line_color")
        else:
            from pyavis.shared.util import color
            color._check_color(line_color)
        
        self._abstract_set_style(line_color)

    def _abstract_set_style(self, line_color: Any):
        pass

    def _abstract_set_line_angle(self):
        pass