
from typing import Tuple

from overrides import override
from pyavis.backends.bases.graphic_bases_v2.rectangle import Rectangle

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
from pyqtgraph.GraphicsScene.mouseEvents import *

class M_RectangleQt(type(Rectangle), type(pg.GraphicsObject)): pass
class RectangleQt(Rectangle, pg.GraphicsObject, metaclass=M_RectangleQt):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            width: float = 1.0,
            height: float = 1.0,
    ):
        Rectangle.__init__(self, position, width, height)
        pg.GraphicsObject.__init__(self)

        self.rectangle = QtWidgets.QGraphicsRectItem(*position, *(self.rect_width, self.rect_height))
        self.rectangle.setParentItem(self)

    def _update_plot(self):
        self.rectangle.setRect(*self.position, *(self.rect_width, self.rect_height))

    def _abstract_set_width(self):
        self._update_plot()

    def _abstract_set_height(self):
        self._update_plot()

    def _abstract_set_position(self):
        self._update_plot()

    def _abstract_set_active(self):
        if self.active:
            self.show()
        else:
            self.hide()
    

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
        return self.rectangle.boundingRect()

    

    
