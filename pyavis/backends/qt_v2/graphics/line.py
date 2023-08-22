
from overrides import override
import pyqtgraph as pg

from pyavis.backends.bases.graphic_bases import Line

class M_LineQt(type(Line), type(pg.InfiniteLine)): pass
class LineQt(Line, pg.InfiniteLine, metaclass=M_LineQt):
    def __init__(self, pos, angle):
        Line.__init__(self, pos, angle)
        pg.InfiniteLine.__init__(self, pos=pos, angle=angle)

    @override
    def set_position(self, x: int | float, y: int | float):
        super().set_position(x, y)
        self.setValue(self.position)

    @property
    @override
    def line_angle(self):
        return super().line_angle
    
    @line_angle.setter
    @override
    def line_angle(self, angle):
        super().line_angle = angle
        self.setAngle(self.line_angle)
        self.angleChanged(self, angle)

    @override
    def set_style(self, style):
        self.setPen(style)

