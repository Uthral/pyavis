from typing import List, Literal, Tuple
from overrides import override

from pyqtgraph.Qt import QtCore, QtWidgets
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg
import numpy as np


from pyavis.shared.util import Subject
from pyavis.graphics import GraphicElement, Rectangle, Selection, Signal, Track, Axis

from .signal import SignalQt
from .rectangle import RectangleQt


class M_TrackQt(type(Track), type(pg.GraphicsObject)): pass
class TrackQt(Track, pg.PlotItem, metaclass=M_TrackQt):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(self, label, sampling_rate):
        pg.PlotItem.__init__(self)
        self.draggable = False
        self.clickable = False

        self.label = label
        self.sampling_rate = sampling_rate

        self.elements: List[GraphicElement] = []
        self.selection: Selection = None

        self.x_movement = False
        self.y_movement = False

    @override
    def add_signal(self, position: Tuple[float, float], data: np.ndarray) -> Signal:
        '''
        Add a new signal to the track.

        Parameters
        ----------
        position : (int, float)
            Position of the signal. Format: (x, y)
        data : np.ndarray
            Data array containing the signal values
        '''
        signal = SignalQt(position=position, data=data)
        self.elements.append(signal)
        self.addItem(signal)

        signal.sigDragged.connect(lambda sig, ev: self._move_on_drag(sig, ev))

        return signal
    
    @override
    def add_rectangle(self, position: Tuple[float, float], size: Tuple[float, float]) -> Rectangle:
        rectangle = RectangleQt(position, size)
        self.elements.append(rectangle)
        self.addItem(rectangle)

        rectangle.sigDragged.connect(lambda rect, ev: self._move_on_drag(rect, ev))

        return rectangle
    
    def add(self, element: GraphicElement):
        self.elements.append(element)
        self.addItem(element)

        # element.sigDragged.connect(lambda elem, ev: self._move_on_drag(rect, ev))

    @override
    def remove(self, element: GraphicElement):
        '''
        Remove a signal from the track.

        Parameters
        ----------
        signal : Signal
            Signal to remove
        '''
        element.sigDragged.disconnect()
        self.elements.remove(element)
        self.removeItem(element)

    def set_selection(self, selection: Selection):
        '''
        Set the active selection.

        Parameters
        ----------
        selection : Selection
            Selection to use
        '''
        self.selection = selection
        self.addItem(self.selection)

    def get_selection(self) -> Selection | None:
        '''
        Get the current selection, or None if nothing is selected.

        Returns
        -------
        Selection | None
            Active selection or None
        '''
        return self.selection


    def unset_selection(self):
        '''
        Unset the active selection. Does nothing if no selection set.
        '''
        self.selection = None



    @override
    def set_style(self, **kwargs):
        '''
        Set the color of the track.

        Parameters
        ----------
        **kwargs : any
            Keyword arguments for setting the track colors
        '''
        pass
    
    @override
    def allow_dragging(self, along_x: bool, along_y: bool):
        '''
        Enable or disable dragging along an axis.

        Parameters
        ----------
        along_x : bool
            Enable / Disable dragging along x axis.
        along_y : bool
            Enable / Disable dragging along y axis.
        '''
        self.x_movement = along_x
        self.y_movement = along_y

    @override
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

    @override
    def link_track(self, track: 'Track', axis: Literal['x', 'y']='x'):
        '''
        Link either the x or y axis of the track to other track.
        None unlinks the track.

        Parameters
        ----------
        track : Track | None
            Track to link with, or None to unlink
        axis : {'x', 'y'}
            Axis to link / unlink
        '''
        if axis == 'x':
            self.getViewBox().setXLink(track.getViewBox() if track is not None else None)
        elif axis == 'y':
            self.getViewBox().setYLink(track.getViewBox() if track is not None else None)
        else:
            raise ValueError("Not a valid axis")

    def set_view_limits(self, **kwargs):
        '''
        Set view limits. Arguments must correspond to accepted arguments of
        `pg.ViewBox.setLimits`

        Parameters
        ----------
        **kwargs
            Arguments to limit view
        '''
        self.getViewBox().setLimits(**kwargs)

    def set_axis(self, axis: Axis):
        '''
        Set the axes of the track.

        Parameters
        ----------
        axis : Axis
            ...
        '''
        self.setAxisItems({axis.orientation : axis})

    








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


    def _move_on_drag(self, elem: GraphicElement, ev: MouseDragEvent):
        if self.x_movement != True and self.y_movement != True:
            return
        
        if elem.draggable != True:
            return
        ev.accept()

        old_pos = elem.position
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

        elem.set_position(*tuple(new_pos))









    def as_widget(self):
        return pg.PlotWidget(plotItem=self)
