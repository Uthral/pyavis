import numpy as np
import pyqtgraph as pg
import PySide2

from overrides import override
from PySide2 import QtWidgets, QtCore
from pyqtgraph.GraphicsScene.mouseEvents import *



class SignalRenderer(pg.GraphicsObject):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(self, start: int, signal: np.ndarray):
        super(SignalRenderer, self).__init__()
        self.clickable = False
        self.draggable = False
        self.signal = signal
        self.start = start
        self.end = start + len(signal)
        self.line_graph = pg.PlotDataItem(x=range(start, len(signal) + start), y=signal)

        (x,y,w,h) = self._calculateRectangleBounds(start, signal)
        self.background_rect = QtWidgets.QGraphicsRectItem(x,y,w,h)
        self._setRectangleStyle()

        self.line_graph.setParentItem(self)
        self.background_rect.setParentItem(self)
        

    def _setRectangleStyle(self):
        c1, c2, c3 = np.random.random(), np.random.random(), np.random.random()
        color_fill = pg.hsvColor(c1, c2, c3, 0.2)
        color_border = pg.hsvColor(c1, c2, c3, 1.0)
        self.background_rect.setPen(pg.mkPen(color_border,width=0))
        self.background_rect.setBrush(pg.mkBrush(color_fill))

    def _calculateRectangleBounds(self, start: int, signal: np.ndarray):
        yMin = np.min(signal)
        yMax = np.max(signal)
        x, y = start, yMin
        width, height = signal.size, yMax - yMin
        return (x, y, width, height)
    
    def update_start(self, new_start:int):
        self.start = new_start
        self.end = self.start + len(self.signal)
        self.line_graph.setData(x=range(self.start, len(self.signal) + self.start), y=self.signal)

        # Update rectanlge
    
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

