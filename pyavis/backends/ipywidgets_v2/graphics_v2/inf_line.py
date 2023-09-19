

from typing import Any, Tuple
from math import cos, sin

from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from overrides import override
from pyavis.backends.bases.graphic_bases_v2.inf_line import InfLine


class InfLineIPY(InfLine):
    def __init__(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            angle: float = 0.0, 
            **kwargs
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
        if 'ax' not in kwargs:
            raise KeyError("Axes not provided. Cannot instantiate SignalIPY.")
        
        InfLine.__init__(self, position, angle)
        self._ax: Axes = kwargs['ax']
        self._line = self._ax.axline(xy1=self.position, xy2=self._calc_pos2())

        self.set_style("default")

    def remove(self):
        self._line.remove()
        self._line = None
        self._ax = None

    def _calc_pos2(self):
        # Calculate position on unit circle and add it together with the position
        # to get the needed second position 
        unit_circle_pos = (cos(self.line_angle), sin(self.line_angle))
        return tuple(map(lambda i,j: i + j, self.position, unit_circle_pos))

    
    def _update_plot(self):
        self._line.remove()
        self._line = self._ax.axline(xy1=self.position, xy2=self._calc_pos2())
        self._line.axes.figure.canvas.draw_idle()

    @override
    def _abstract_set_active(self):
        self._line.set_visible(self.active)
        self._line.axes.figure.canvas.draw_idle()
    
    @override
    def _abstract_set_position(self):
        self._update_plot()

    @override
    def _abstract_set_angle(self):
        self._update_plot()

    @override
    def _abstract_set_style(self, line_color: Any):
        from pyavis.shared.util import color
        line_color = color._convert_color(line_color)
        self._line.set_color(line_color)

