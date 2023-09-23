from typing import Literal, Tuple

from pyqtgraph.Qt import QtCore
from overrides import override
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg
from pyavis.backends.bases.graphic_bases import Signal

class M_SignalQt(type(Signal), type(pg.GraphicsObject)): pass
class SignalQt(Signal, pg.GraphicsObject, metaclass=M_SignalQt):

    def __init__(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            vertical_size: Literal["auto"] = "auto",
            *args,
            **kwargs
    ):
        Signal.__init__(self, position, vertical_size, *args, **kwargs)
        pg.GraphicsObject.__init__(self)
        
        self.signal = pg.PlotDataItem()
        self.signal.setParentItem(self)

        self.set_style("default")
        self._update_plot()

    def _update_plot(self):
        if self.y_data is not None and self.x_data is not None:
            self.signal.setData(x=self.x_data + self.position[0], y=self.y_data_sized + self.position[1])

    @override
    def _abstract_set_active(self):
        if self.active:
            self.show()
        else:
            self.hide()
    
    @override
    def _abstract_set_data(self):
        self._update_plot()
    
    @override
    def _abstract_set_position(self):
        self._update_plot()
    
    @override
    def _abstract_set_vertical_size(self):
        self._update_plot()



    def _abstract_set_style(self, line_color):
        from pyavis.shared.util import color
        line_color = color._convert_color(line_color)
        self.signal.setPen(pg.mkPen(pg.mkColor(*line_color), width=0))


        

    def mouseClickEvent(self, ev: MouseClickEvent):
        if self.clickable != True:
            return
        ev.accept()
        self.sigClicked.emit(self, ev)

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

    @override
    def boundingRect(self):
        return self.signal.curve.boundingRect()