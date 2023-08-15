from overrides import override
from typing import List, Tuple, Any

from pyavis.base_classes import BaseTrack
from pyavis.shared import AudioSignal
from pyavis.shared.multitrack import Track

from pyqtgraph.Qt import QtCore, QtWidgets
from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg
import numpy as np

class M_TrackQt(type(BaseTrack), type(pg.PlotItem)): pass
class TrackQt(BaseTrack, pg.PlotItem, metaclass=M_TrackQt):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    @override
    def __init__(self, label: str, sampling_rate: int, **kwargs):
        pg.PlotItem.__init__(self, **kwargs)

        self.label = label
        self.sampling_rate = sampling_rate

        self.clickable = False
        self.draggable = False

        self.track = Track(label, sampling_rate)
        self.signal_renderers: List[Tuple[Any, _Signal]] = []
        
        self._calculateViewLimits()
        self._addMiddleLine()
        
    @override
    def add_signal(self, position: int, signal, **kwargs):
        success = self.track.try_add(position, signal)
        if not success:
            raise ValueError("Could not add signal")

        signal_render = _Signal(position, signal)
        self.getViewBox().addItem(signal_render)

        self.signal_renderers.append((signal, signal_render))

    @override
    def remove_signal(self, signal):
        (position, signal) = self.track.get_signal(signal)
        success = self.track.remove(position, signal)
        if not success:
            raise ValueError("Could not remove signal")

        result = next(filter(lambda item: item[0] == signal, self.signal_renderers), None)
        (signal, signal_renderer) = result

        self.getViewBox().removeItem(signal_renderer)
        self.signal_renderers.remove(result)

    @override
    def remove_at_position(self, position: int):
        result = self.track.get_signal_at_position(position)
        if result is None:
            raise ValueError("Could not remove signal")
        
        (position, signal) = result
        self.track.remove(position, signal)

        result = next(filter(lambda item: item[0] == signal, self.signal_renderers), None)
        (signal, signal_renderer) = result

        self.getViewBox().removeItem(signal_renderer)
        self.signal_renderers.remove(result)

    @override
    def __getitem__(self, index):
        return self.track[index]
    
    def _addMiddleLine(self, color="r"):
        """
        Add an horizontal :class:`InfiniteLine <pyqtgraph.InfiniteLine>` to the track, seperating positive and negative numbers.

        Parameters
        ----------
        color : any
            Forwarded to :func:`mkColor <pyqtgraph.mkColor>`
        """
        line = pg.InfiniteLine(angle=0, pos=0, pen=pg.mkPen(color='r'))
        line.setZValue(10)
        self.getViewBox().addItem(line)

    def _calculateViewLimits(self, padding: float = 0.1):
        """ 
        Calculate the limits of the :class:`ViewBox <pyqtgraph.ViewBox>` of the display based
        on the signal data.

        Parameters
        ----------
        padding : float, default: 0.1
            Padding added to y-Axis
        """
        xMin = 0
        yMin = -1.0 - padding
        yMax = 1.0 + padding 
        yRange = np.abs(yMax) + np.abs(yMin)

        self.getViewBox().setLimits(xMin=xMin, yMin=yMin, yMax=yMax, minYRange=yRange, maxYRange=yRange)

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


class _Signal(pg.GraphicsObject):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(self, start: int, signal: AudioSignal, *args, **kwargs):
        super(_Signal, self).__init__(*args)
        self.start = start
        self.end = start + len(signal.signal())
        self.signal = signal

        self.clickable = False
        self.draggable = False

        self._setBackgroundRect()
        self.line_graph = pg.PlotDataItem(x=range(start, len(signal.signal()) + start), y=signal.signal())

        self.background_rect.setParentItem(self)
        self.line_graph.setParentItem(self)

    @override
    def boundingRect(self):
        return self.background_rect.boundingRect()
    
    def _setBackgroundRect(self, border_color=None, background_color=None):
        """
        Set the background rectangle of the signal based on the signal data.

        Parameters
        ----------
        border_color : Any
            Forwarded to :func:`mkPen <pyqtgraph.mkPen>`
        background_color : Any
            Forwarded to :func:`mkBrush <pyqtgraph.mkBrush>`
        """
        (x,y,w,h) = self._calculateRectangleBounds()
        self.background_rect = QtWidgets.QGraphicsRectItem(x,y,w,h)
        self._setRectangleStyle(border_color, background_color)
    
    def _calculateRectangleBounds(self):
        yMin = -1 # np.min(self.signal.signal)
        yMax = 1  # np.max(self.signal.signal)
        x, y = self.start, yMin
        width, height = len(self.signal.signal()), yMax - yMin
        return (x, y, width, height)
    
    def _setRectangleStyle(self, border_color=None, background_color=None):
        """
        Set the style of the background rectangle.

        Parameters
        ----------
        border_color : Any
            Forwarded to :func:`mkPen <pyqtgraph.mkPen>`
        background_color : Any
            Forwarded to :func:`mkBrush <pyqtgraph.mkBrush>`
        """
        if border_color is None and background_color is None:
            c1, c3 = np.random.random(), np.random.random()
            background_color = pg.hsvColor(c1, 1, c3, 0.2)
            border_color = pg.hsvColor(c1, 1, c3, 1.0)
        self.background_rect.setPen(pg.mkPen(border_color,width=0))
        self.background_rect.setBrush(pg.mkBrush(background_color))

    def setClickable(self, value: bool):
        self.clickable = value

    def setDraggable(self, value: bool):
        self.draggable = value

    def updatePosition(self, newStart: int):
        (x,y,w,h) = self._calculateRectangleBounds()
        self.background_rect.update(newStart, y, w, h)
        self.line_graph.curve.setData(x=range(newStart, len(self.signal.signal()) + newStart), y=self.signal.signal())

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