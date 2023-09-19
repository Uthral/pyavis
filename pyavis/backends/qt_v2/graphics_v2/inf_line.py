
import math
from typing import Any, Tuple
from overrides import override

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.GraphicsScene.mouseEvents import *

from pyavis.backends.bases.graphic_bases_v2.inf_line import InfLine

class M_InfLineQt(type(InfLine), type(pg.InfiniteLine)): pass
class InfLineQt(InfLine, pg.InfiniteLine, metaclass=M_InfLineQt):

    def __init__(            
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            angle: float = 0.0, 
    ):
        InfLine.__init__(self, position, angle)
        pg.InfiniteLine.__init__(self, pos=self.position, angle=int(math.degrees(self.line_angle)))

        self.set_style("default")

    
    def _update_plot(self):
        self.setPos(self.position)
        self.setAngle(int(math.degrees(self.line_angle)))


    def _abstract_set_active(self):
        if self.active:
            self.show()
        else:
            self.hide()
    
    def _abstract_set_position(self):
        self._update_plot()

    def _abstract_set_angle(self):
        self._update_plot()

    def _abstract_set_style(self, line_color: Any):
        from pyavis.shared.util import color
        line_color = color._convert_color(line_color)
        self.setPen(pg.mkPen(pg.mkColor(*line_color), width=0))


    def mouseClickEvent(self, ev: MouseClickEvent):
        if self.clickable != True:
            return
        ev.accept()

        self.onClick.emit(self)

    def mouseDragEvent(self, ev: MouseDragEvent):
        if self.draggable != True:
            return
        ev.accept()

        if ev.isStart():
            self.onDraggingBegin.emit(self, ev.pos())
        elif ev.isFinish():
            self.onDraggingFinish.emit(self, ev.pos())
        else:
            self.onDragging.emit(self, ev.pos())
