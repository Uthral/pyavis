from typing import Tuple, Any

from pyqtgraph.Qt import QtCore, QtWidgets
from overrides import override
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg
import numpy as np

from pyavis.graphics import Signal
from pyavis.shared.util import Subject


class M_SignalQt(type(Signal), type(pg.GraphicsObject)): pass

class SignalQt(Signal, pg.GraphicsObject, metaclass=M_SignalQt):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(
            self,
            position: Tuple[int, float],
            data: np.ndarray,
            sig_size: float | str = 'auto',
            rect_size: float | str = 'auto',
    ):
        pg.GraphicsObject.__init__(self)
        self.draggable = False
        self.clickable = False

        self.position = position
        self.data = data

        self.signal_size = sig_size
        self.orig_signal_size = np.max(data)
        self._handle_signal_size()

        self.rectangle_size = rect_size
        self._handle_rectanlge_size()
        self.show_rect=True

        self.bound_rect = QtWidgets.QGraphicsRectItem(*self._calc_rect_bounds())
        self.line_plot = pg.PlotDataItem(
            x=range(self.position[0], len(self.data) + self.position[0]),
            y=self.data + self.position[1]
        )

        self.bound_rect.setParentItem(self)
        self.line_plot.setParentItem(self)

    @override
    def set_data(self, data):
        self.data = data
        self.orig_signal_size = np.max(data)
        self._handle_signal_size()
        self._handle_rectanlge_size()
        self._update_plot(update_lines=True, update_rect=True)
    
    @override
    def set_signal_size(self, size: float | str = "auto"):
        '''
        Set the y-size of the signal. "auto" uses the orignal values as size.

        Parameters:
        -----------
        size : float | str, default: "auto"
            New y-size of the rendered signal
        '''
        
        if self.signal_size == size:
            return
        else:
            self.signal_size = size
            self._handle_signal_size()
            self._update_plot(update_lines=True)

    def _handle_signal_size(self):
        def norm(data):
            return data / np.max(data)
        
        if self.signal_size == "auto":
            self.data = norm(self.data) * self.orig_signal_size
        else:
            self.data = norm(self.data) * (self.signal_size / 2)

    @override
    def set_rectangle_size(self, size: float | str = "auto"):
        '''
        Set the size of the rectangle. "auto" uses the min & max value of the data.

        Parameters:
        -----------
        size : float | "auto", default: "auto"
            New size of the rendered bounding rectangle
        '''
        if self.rectangle_size == size:
            return
        else:
            self.rectangle_size = size
            self._handle_rectanlge_size()
            self._update_plot(update_rect=True)
        

    def _handle_rectanlge_size(self): 
        if self.rectangle_size == "auto":
            self.rectangle_width = len(self.data)
            self.rectangle_height = np.max(self.data) - np.min(self.data)
        else:
            self.rectangle_width = len(self.data)
            self.rectangle_height = self.rectangle_size

    @override
    def update_position(self, position: Tuple[int, float]):
        '''
        Update the position of the signal.

        Parameters
        ----------
        position : (int, float)
            New position of the signal. Format: (x, y)
        '''
        self.position = position
        self._update_plot(update_rect=True, update_lines=True)

    @override
    def set_style(self, signal_style: Any | str = "default", rect_style: dict | str = "default"):
        '''
        Set the color of the signal and the bounding rectangle.

        Parameters
        ----------
        signal_kw : Any | str, default: "default"
            Either "default" or values accepted by `pg.mkColor`
        rect_kw : dict | str, default: "default"
            Allowed arguments: "fill" and "border". Must correspond to values accepted by `pg.mkColor`
        '''
        default_color = (200, 200, 200)

        if signal_style == "default":
            self.line_plot.setPen(pg.mkPen(pg.mkColor(*default_color), width=0))
        else:
            self.line_plot.setPen(pg.mkPen(pg.mkColor(signal_style), width=0))

        if rect_style == "default":
            self.bound_rect.setBrush(pg.mkBrush(pg.mkColor(*default_color, 50)))
            self.bound_rect.setPen(pg.mkPen(pg.mkColor(*default_color, 255), width=0))
        else:
            fill_color = rect_style["fill"]
            border_color = rect_style["border"]

            self.bound_rect.setBrush(pg.mkBrush(pg.mkColor(*fill_color)))
            self.bound_rect.setPen(pg.mkPen(pg.mkColor(*border_color), width=0))
    

    @override
    def toggle_rectangle(self, show_rect: bool = False):
        '''
        Hide or show the background rectangle.

        Parameters
        ----------
        show_rect : bool, default: False
            Hide or show rectangle
        '''
        if self.show_rect == show_rect:
            return

        self.show_rect = show_rect
        self._update_plot(update_rect=True)




    def _calc_rect_bounds(self):
        x = self.position[0]
        if self.rectangle_size == "auto":
            y = np.min(self.data)
        else:
            y = self.position[1] - self.rectangle_height / 2

        return (x, y, self.rectangle_width, self.rectangle_height)
    
    def _update_plot(self, update_lines = False, update_rect = False):
        if update_rect:
            self.bound_rect.setRect(*self._calc_rect_bounds())
            self.bound_rect.setVisible(self.show_rect)

        if update_lines:
            self.line_plot.setData(x=range(self.position[0], len(self.data) + self.position[0]), y=self.data + self.position[1])
            



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
        return self.bound_rect.boundingRect()