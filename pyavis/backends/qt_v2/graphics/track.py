from typing import List, Literal, Tuple
from overrides import override

from pyqtgraph.Qt import QtCore, QtWidgets
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg
import numpy as np


from pyavis.shared.util import Subject
from pyavis.backends.bases.graphic_bases import GraphicElement, Rectangle, Selection, Signal, Track, Axis

from .signal import SignalQt
from .rectangle import RectangleQt


class M_TrackQt(type(Track), type(pg.PlotItem)): pass
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
        signal = SignalQt(position, "auto", data)
        self.elements.append(signal)
        self.addItem(signal)

        signal.sigDragged.connect(lambda sig, ev: self._move_on_drag(sig, ev))

        return signal
    
    def add_rectangle(self, position: Tuple[float, float], size: Tuple[float, float]) -> Rectangle:
        rectangle = RectangleQt(position, size)
        self.elements.append(rectangle)
        self.addItem(rectangle)

        rectangle.sigDragged.connect(lambda rect, ev: self._move_on_drag(rect, ev))

        return rectangle
    
    def add(self, element: GraphicElement):
        self.elements.append(element)
        self.addItem(element)

    def remove(self, element: GraphicElement):
        element.sigDragged.disconnect()
        self.elements.remove(element)
        self.removeItem(element)

    def set_selection(self, selection: Selection):
        self.selection = selection
        self.addItem(self.selection)

    def get_selection(self) -> Selection | None:
        return self.selection


    def unset_selection(self):
        self.selection = None



    def set_style(self, **kwargs):
        pass
    
    def allow_dragging(self, along_x: bool, along_y: bool):
        self.x_movement = along_x
        self.y_movement = along_y

    def set_dragging_limits(
            self,
            x_limits: Tuple[int | None, int | None] = (None, None),
            y_limits: Tuple[float | None, float | None] = (None, None)
    ):
        self.x_limits = x_limits
        self.y_limits = y_limits

    def link_track(self, track: 'Track', axis: Literal['x', 'y']='x'):
        if axis == 'x':
            self.getViewBox().setXLink(track.getViewBox() if track is not None else None)
        elif axis == 'y':
            self.getViewBox().setYLink(track.getViewBox() if track is not None else None)
        else:
            raise ValueError("Not a valid axis")

    def set_view_limits(self, **kwargs):
        self.getViewBox().setLimits(**kwargs)

    def set_axis(self, axis: Axis):
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
