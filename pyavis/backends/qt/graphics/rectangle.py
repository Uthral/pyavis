
from typing import Tuple
from pyavis.backends.bases.graphic_bases.rectangle import Rectangle

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
from pyqtgraph.GraphicsScene.mouseEvents import *

class M_RectangleQt(type(Rectangle), type(pg.GraphicsObject)): pass
class RectangleQt(Rectangle, pg.GraphicsObject, metaclass=M_RectangleQt):

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

        self.set_style("default", "default")

    def _update_plot(self):
        self.rectangle.setRect(*self.position, *(self.rect_width, self.rect_height))

    def _abstract_set_position(self):
        self._update_plot()

    def _abstract_set_size(self):
        self._update_plot()

    def _abstract_set_active(self):
        if self.active:
            self.show()
        else:
            self.hide()
        
    def _abstract_set_style(self, border_color, fill_color):
        from pyavis.shared.util import color
        border_color = color._convert_color(border_color)
        fill_color = color._convert_color(fill_color)
        
        self.rectangle.setBrush(pg.mkBrush(pg.mkColor(*fill_color)))
        self.rectangle.setPen(pg.mkPen(pg.mkColor(*border_color), width=0))
    

    def mouseClickEvent(self, ev: MouseClickEvent):
        if self.clickable != True:
            return
        ev.accept()

        viewPos = self.getViewBox().mapSceneToView(ev.scenePos())
        self.onClick.emit(self, (viewPos.x(), viewPos.y()))

    def mouseDragEvent(self, ev: MouseDragEvent):
        if self.draggable != True:
            return
        ev.accept()

        viewPos = self.getViewBox().mapSceneToView(ev.scenePos())
        if ev.isStart():
            self.onDraggingBegin.emit(self, (viewPos.x(), viewPos.y()))
        elif ev.isFinish():
            self.onDraggingFinish.emit(self, (viewPos.x(), viewPos.y()))
        else:
            self.onDragging.emit(self, (viewPos.x(), viewPos.y()))

    def boundingRect(self):
        return self.rectangle.boundingRect()


    
