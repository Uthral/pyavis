import pyqtgraph as pg
import numpy as np

from typing import Literal, Tuple

from pyqtgraph.Qt import QtCore, QtWidgets
from overrides import override
from pyqtgraph.GraphicsScene.mouseEvents import *

from pyavis.graphics import Rectangle


class M_RectangleQt(type(Rectangle), type(pg.GraphicsObject)): pass
class RectangleQt(Rectangle, pg.GraphicsObject, metaclass=M_RectangleQt):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(
            self,
            position: Tuple[float, float],
            size: Tuple[float, float],
            style: dict | Literal["default"] = "default",
    ):
        Rectangle.__init__(self)
        pg.GraphicsObject.__init__(self)

        self.draggable = False
        self.clickable = False

        self.active=True

        self.position = position
        self.size = size
        self.style = style

        self.rect = QtWidgets.QGraphicsRectItem(*position, *size)
        self.rect.setParentItem(self)

        self.set_style(style)

    @override
    def set_size(self, width: float, height: float):
        '''
        Set the size of the rectangle.

        Parameters:
        -----------
        size : (float, float)
            New size of the rectangle. Format: (width, height)
        '''

        old_size = self.size
        new_size = (width, height)
        self.size = new_size
        self._update_plot()

        self.sizeChanged.emit(self, new_size, old_size)

    @override
    def set_position(self, x: int | float, y: int | float):
        '''
        Update the position of the rectangle.

        Parameters
        ----------
        position : (float, float)
            New position of the rectangle. Format: (x, y)
        '''
        super().set_position(x,y)
        self._update_plot()
    
    @override
    def set_active(self, active: bool = False):
        '''
        Hide or show the rectangle.

        Parameters
        ----------
        active : bool, default: False
            Hide or show rectangle
        '''
        super().set_active(active)
        self._update_plot()

    @override
    def set_style(self, style: dict | Literal["default"] = "default"):
        '''
        Set the color of the rectangle.

        Parameters
        ----------
        style : dict | str, default: "default"
            Allowed dict arguments: "fill" and "border". Must correspond to values accepted by `pg.mkColor`
        '''
        default_color = (200, 200, 200)

        if style == "default":
            self.rect.setBrush(pg.mkBrush(pg.mkColor(*default_color, 50)))
            self.rect.setPen(pg.mkPen(pg.mkColor(*default_color, 255), width=0))
        else:
            fill_color = style["fill"]
            border_color = style["border"]

            self.rect.setBrush(pg.mkBrush(pg.mkColor(*fill_color)))
            self.rect.setPen(pg.mkPen(pg.mkColor(*border_color), width=0))
    
    def _update_plot(self):
        self.rect.setRect(*self.position, *self.size)
        self.rect.setVisible(self.active)



















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

    @override
    def boundingRect(self):
        return self.rect.boundingRect()

        