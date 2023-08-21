from typing import Literal, Tuple, Any

from pyqtgraph.Qt import QtCore, QtWidgets
from overrides import override
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg
import numpy as np

from pyavis.backends.bases.graphic_bases import Signal
from pyavis.shared.util import Subject


class M_SignalQt(type(Signal), type(pg.GraphicsObject)): pass

class SignalQt(Signal, pg.GraphicsObject, metaclass=M_SignalQt):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(
            self,
            position: Tuple[int, float] = (0,0),
            vert_size: float | Literal["auto"] = 'auto',
            *args,
            **kwargs,
    ):
        '''
        Initalize a new signal renderer.

        Parameter
        ---------
        position: (int, float), default: (0,0)
            Position of the rendered signal. y position equates to a y value of 0.
        sig_size: float | "auto", default: "auto
            Vertical size of the data.
        *args
            Passed to ``:func:Signal.set_data()``
        **kwargs
            Passed to ``:func:Signal.set_data()``
            
        '''
        Signal.__init__(self)
        pg.GraphicsObject.__init__(self)
        self.draggable = False
        self.clickable = False

        self.position = position
        super().set_data(*args, **kwargs)

        self.vert_size = vert_size
        self.orig_vert_size = np.max(self.y_data)
        self._handle_signal_size()

        self.line_plot = pg.PlotDataItem(
            x=self.x_data + self.position[0],
            y=self.y_data + self.position[1]
        )

        self.line_plot.setParentItem(self)

    @override
    def set_data(self, *args, **kwargs):
        super().set_data(*args, **kwargs)
        self.orig_vert_size = np.max(self.y_data)
        self._handle_signal_size()
        self._update_plot()

        self.dataChanged.emit(self)
    
    @override
    def set_vertical_size(self, size: float | Literal["auto"] = "auto"):
        if self.vert_size == size:
            return
        else:
            self.vert_size = size
            self._handle_signal_size()
            self._update_plot()

    def _handle_signal_size(self):
        def norm(data):
            return data / np.max(data)
        
        if self.vert_size == "auto":
            self.y_data = norm(self.y_data) * self.orig_vert_size
        else:
            self.y_data = norm(self.y_data) * (self.vert_size / 2)

    @override
    def set_position(self, x: int | float, y: int | float):
        '''
        Update the position of the signal.

        Parameters
        ----------
        position : (int, float)
            New position of the signal. Format: (x, y)
        '''
        super().set_position(int(x), y)
        self._update_plot()

    @override
    def set_active(self, active: bool = False):
        '''
        Hide or show the signal.

        Parameters
        ----------
        active : bool, default: False
            Hide or show signal
        '''
        super().set_active(active)
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
    
    def _update_plot(self):
        self.line_plot.setData(x=self.x_data + self.position[0], y=self.y_data + self.position[1])


    def mouseClickEvent(self, ev: MouseClickEvent):
        if self.clickable != True:
            return
        ev.accept()
        self.sigClicked.emit(self, ev)

        self.click.emit()

    def mouseDragEvent(self, ev: MouseDragEvent):
        if self.draggable != True:
            return
        ev.accept()
        self.sigDragged.emit(self, ev)

        if ev.isStart():
            self.draggingBegin.emit(self, ev.pos())
        elif ev.isFinish():
            self.draggingFinish.emit(self, ev.pos())
        else:
            self.dragging.emit(self, ev.pos())
    
    def hoverEvent(self, ev: HoverEvent):
        self.sigHovered.emit(self, ev)

    @override
    def boundingRect(self):
        return self.line_plot.curve.boundingRect()