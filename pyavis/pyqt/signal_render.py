import numpy as np
import pyqtgraph as pg
import PySide2
import pya

from overrides import override
from PySide2 import QtWidgets, QtCore
from pyqtgraph.GraphicsScene.mouseEvents import *


class SignalRender(pg.GraphicsObject):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(self, audio: pya.Asig):
        super(SignalRender, self).__init__()
        self.clickable = False
        self.draggable = False
        self.line_graph = pg.PlotDataItem(y=audio.sig)

        (x,y,w,h) = self._calculateRectangleBounds(audio)
        self.background_rect = QtWidgets.QGraphicsRectItem(x,y,w,h)
        self._setRectangleStyle()

        self.line_graph.setParentItem(self)
        self.background_rect.setParentItem(self) 

        print(self.clickable)
        print(self.draggable)
        

    def _setRectangleStyle(self):
        c1, c2, c3 = np.random.random(), np.random.random(), np.random.random()
        color_fill = pg.hsvColor(c1, c2, c3, 0.2)
        color_border = pg.hsvColor(c1, c2, c3, 1.0)
        self.background_rect.setPen(pg.mkPen(color_border,width=0))
        self.background_rect.setBrush(pg.mkBrush(color_fill))

    def _calculateRectangleBounds(self, audio: pya.Asig):
        yMin = np.min(audio.sig)
        yMax = np.max(audio.sig)
        x, y = 0, yMin
        width, height = audio.samples, yMax - yMin
        return (x, y, width, height)
    
    def setClickable(self, value: bool):
        self.clickable = value

    def setDraggable(self, value: bool):
        self.draggable = value

    @override
    def boundingRect(self):
        return self.background_rect.boundingRect()
    
    def paint(self, painter: PySide2.QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget | None = ...) -> None:
        pass
    
    def mouseClickEvent(self, ev: MouseClickEvent):
        if self.clickable != True:
            return
        ev.accept()
        self.sigClicked.emit(self, ev)

    def mouseDragEvent(self, ev: MouseDragEvent):
        if self.draggable != True:
            return
        ev.accept()
        self.sigDragged.emit(self, ev)
    
    def hoverEvent(self, ev: HoverEvent):
        self.sigHovered.emit(self, ev)

