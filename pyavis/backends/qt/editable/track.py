from typing import List, Tuple

from pyqtgraph.Qt import QtCore, QtWidgets
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg
import numpy as np

from pyavis.shared.util import Subject

from .signal import SignalQt

class TrackQt(pg.PlotItem):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(self, label, sampling_rate):
        pg.PlotItem.__init__(self)
        self.draggable = False
        self.clickable = False

        # self.onSignalMoved = Subject()
        # self.onSignalResized = Subject()
        # self.onSignalAdded = Subject()
        # self.onSignalRemoved = Subject()

        self.label = label
        self.sampling_rate = sampling_rate

        self.signals: List[SignalQt]  = []
        self.x_movement = False
        self.y_movement = False

    def add_signal(self, position: Tuple[int, float], data: np.ndarray) -> SignalQt:
        '''
        Add a new signal to the track.

        Parameters
        ----------
        position : (int, float)
            Position of the signal. Format: (x, y)
        data : np.ndarray
            Data array containing the signal values
        signal_kw : dict
            ... 
        '''
        signal = SignalQt(position=position, data=data)
        self.signals.append(signal)
        self.addItem(signal)

        return signal

    def remove_signal(self, signal):
        '''
        Remove a signal from the track.

        Parameters
        ----------
        signal : Signal
            Signal to remove
        '''
        self.signals.remove(signal)
        self.removeItem(signal)

    def set_style(self, **kwargs):
        '''
        Set the color of the track.

        Parameters
        ----------
        **kwargs : any
            Keyword arguments for setting the track colors
        '''
        pass

    def allow_signal_dragging(self, along_x: bool, along_y: bool):
        '''
        Enable or disable dragging along an axis.

        Parameters
        ----------
        along_x : bool
            Enable / Disable dragging along x axis.
        along_y : bool
            Enable / Disable dragging along y axis.
        '''

        # Check if signals are overall allowed to be dragged
        # Disable signal dragging if no dragging along any axis is allowed
        prev_dragging_state = self.x_movement or self.y_movement
        curr_dragging_state = along_x or along_y

        if curr_dragging_state != prev_dragging_state:
            for signal in self.signals:
                signal.draggable = curr_dragging_state
                if signal.draggable:
                    signal.sigDragged.connect(lambda sig, ev: self._move_signal_on_drag(sig, ev))
                else:
                    signal.sigDragged.disconnect()

        self.x_movement = along_x
        self.y_movement = along_y

    def set_dragging_limits(
            self,
            x_limits: Tuple[int | None, int | None] = (None, None),
            y_limits: Tuple[float | None, float | None] = (None, None)
    ):
        '''
        Set the limits in which the signals can be dragged.

        Parameters
        ----------
        x_limits : (int | None, int | None), default: (None, None)
            Lower and upper limit: (lower, upper)
        y_limits : (float | None, float | None), default: (None, None)
            Lower and upper limit: (lower, upper)
        '''
        self.x_limits = x_limits
        self.y_limits = y_limits


    def set_axis(self, axis):
        '''
        Set the axes of the track.

        Parameters
        ----------
        axis : any
            ...
        '''
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





    def _move_signal_on_drag(self, sig: SignalQt, ev: MouseDragEvent):
        old_pos = sig.position
        new_pos = list(old_pos)

        if self.x_movement:
            x_pos = int(ev.pos().x())

            if self.x_limits[0] is not None and x_pos < self.x_limits[0]:
                x_pos = self.x_limits[0]
            elif self.x_limits[1] is not None and x_pos > self.x_limits[1]:
                x_pos = self.x_limits[1]
            new_pos[0] = x_pos

        if self.y_movement:
            y_pos = ev.pos().y()

            if self.y_limits[0] is not None and y_pos < self.y_limits[0]:
                y_pos = self.y_limits[0]
            elif self.y_limits[1] is not None and y_pos > self.y_limits[1]:
                y_pos = self.y_limits[1]
            new_pos[1] = y_pos
        
        
        sig.update_position(tuple(new_pos))









    def as_widget(self):
        return pg.PlotWidget(plotItem=self)
