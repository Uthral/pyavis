from typing import Literal,  Any, Tuple

from pyqtgraph.Qt import QtCore
from overrides import override
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg
from pyavis.backends.bases.graphic_bases_v2 import Signal


class M_SignalQt(type(Signal), type(pg.GraphicsObject)): pass
class SignalQt(Signal, pg.GraphicsObject, metaclass=M_SignalQt):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

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

        self._update_plot()

    def _update_plot(self):
        if self.y_data is not None and self.x_data is not None:
            self.signal.setData(x=self.x_data + self.position[0], y=self.y_data_sized + self.position[1])
            print(self.signal.xData)

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








    @override
    def set_style(self, style: Any | Literal["default"] = "default"):
        '''
        Set the color of the signal.

        Parameters
        ----------
        signal_kw : Any | str, default: "default"
            Either "default" or values accepted by `pg.mkColor`
        '''
        default_color = (200, 200, 200)

        if style == "default":
            self.line_plot.setPen(pg.mkPen(pg.mkColor(*default_color), width=0))
        else:
            self.line_plot.setPen(pg.mkPen(pg.mkColor(style), width=0))
    






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
        self.sigDragged.emit(self, ev)

        if ev.isStart():
            self.onDraggingBegin.emit(self, ev.pos())
        elif ev.isFinish():
            self.onDraggingFinish.emit(self, ev.pos())
        else:
            self.onDragging.emit(self, ev.pos())
    
    def hoverEvent(self, ev: HoverEvent):
        self.sigHovered.emit(self, ev)


    @override
    def boundingRect(self):
        return self.signal.curve.boundingRect()