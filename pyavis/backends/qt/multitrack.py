from overrides import override
from typing import List
from ...base_classes import AbstractMultiTrackVisualizer
from ...shared import Signal
from ...shared.multitrack import MultiTrack, Track

from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
from pyqtgraph.GraphicsScene.mouseEvents import *
import pyqtgraph as pg
import numpy as np

class MultiTrackVisualizerQt(AbstractMultiTrackVisualizer):
    def __init__(self, multi_track: MultiTrack, *args, **kwargs):
        self.widget = pg.GraphicsLayoutWidget(**kwargs) 
        self.track_renderes: List[_Track] = []
        self.multi_track = multi_track
        
        self.pannZoom = False
        self.selecting = True

        top_axis = pg.AxisItem("top")
        self.widget.addItem(item=top_axis, row=0, col=1)
        self.widget.nextRow()

        top_track_view = None
        for track in multi_track.tracks:
            trk = _Track(track)
            self.track_renderes.append(trk)
            self.selection = None

            # Share a signle axis at the top
            # TODO: change _Track to View, i.e. no inherent axis
            trk.hideAxis("bottom")
            trk.hideAxis("left")

            if top_track_view is None:
                top_track_view = trk.getViewBox()
                top_axis.linkToView(top_track_view)
            else:
                track_view = trk.getViewBox()
                track_view.setXLink(top_track_view)
            
            trk.sigDragged.connect(self.on_track_dragged)
            trk.sigClicked.connect(self.on_track_clicked)

            track_axis = pg.AxisItem("left")
            track_axis.linkToView(trk.getViewBox())

            self.widget.addItem(item=track_axis, col=0)
            self.widget.addItem(item=trk, col=1)
            self.widget.nextRow()

    def set_pann_and_zoom(self):
        if self.pannZoom is False:
            self.pannZoom = True
            self.selecting = False

            # TODO: Enable panning and zooming in tracks

    def set_selecting(self):
        if self.selecting is False:
            self.pannZoom = False
            self.selecting = True

            # TODO: Enable selection across tracks

    def on_track_clicked(self, track, event: MouseClickEvent):
        if self.selection:
            view = self.plot_item.getViewBox()
            view.removeItem(self.selection)
            self.selection = None

    def on_track_dragged(self, track, event: MouseDragEvent):
        if not self.selection:
            # Track coordinates are not the same as its containing view coords
            # -> Transform scene to view (this will probalbly change when)
            self.start_pos = track.getViewBox().mapSceneToView(event.pos())
            self.selection = pg.LinearRegionItem(values=(self.start_pos.x(), self.start_pos.x()), orientation=pg.LinearRegionItem.Vertical)

            for trk in self.track_renderes:
                # Adds selection only to last track
                # -> use observer pattern to render selections
                trk.addItem(self.selection)

        else:
            event_pos = track.getViewBox().mapSceneToView(event.pos())
            self.selection.setRegion((self.start_pos.x(), event_pos.x()))

    def get_native_widget(self: bool):
        return self.widget

class _Track(pg.PlotItem):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(self, track: Track, *args, **kwargs):
        super(_Track, self).__init__(*args)
        self.signal_renderers = []
        self.track = track

        self.clickable = False
        self.draggable = True

        viewBox = self.getViewBox()
        divider = pg.InfiniteLine(angle=0, pos=0, pen=pg.mkPen(color='r'))

        viewBox.addItem(divider)

        for signal in track.signals:
            sig = _Signal(signal[0], signal[1])
            viewBox.addItem(sig)

        self._calculateViewLimits()
    
    def add_signal(signal):
        pass
    def remove_signal(signal):
        pass

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

        view_box = self.getViewBox()
        view_box.setLimits(xMin=xMin, yMin=yMin, yMax=yMax, minYRange=yRange, maxYRange=yRange) 

    

    def mouseClickEvent(self, ev: MouseClickEvent):
        if self.clickable != True:
            return
        ev.accept()
        print("Hello")
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

    def __init__(self, start: int, signal: Signal, *args, **kwargs):
        super(_Signal, self).__init__(*args)
        self.start = start
        self.end = start + len(signal.signal)
        self.signal = signal

        self.clickable = False
        self.draggable = False

        self.line_graph = pg.PlotDataItem(x=range(start, len(signal.signal) + start), y=signal.signal)

        (x,y,w,h) = self._calculateRectangleBounds()
        self.background_rect = QtWidgets.QGraphicsRectItem(x,y,w,h)
        self._setRectangleStyle()


        self.background_rect.setParentItem(self)
        self.line_graph.setParentItem(self)

    @override
    def boundingRect(self):
        return self.line_graph.curve.boundingRect()
    
    def _calculateRectangleBounds(self):
        yMin = -1 # np.min(self.signal.signal)
        yMax = 1  # np.max(self.signal.signal)
        x, y = self.start, yMin
        width, height = len(self.signal.signal), yMax - yMin
        return (x, y, width, height)
    
    def _setRectangleStyle(self):
        c1, c2, c3 = np.random.random(), np.random.random(), np.random.random()
        color_fill = pg.hsvColor(c1, 1, c3, 0.2)
        color_border = pg.hsvColor(c1, 1, c3, 1.0)
        self.background_rect.setPen(pg.mkPen(color_border,width=0))
        self.background_rect.setBrush(pg.mkBrush(color_fill))

    def setClickable(self, value: bool):
        self.clickable = value

    def setDraggable(self, value: bool):
        self.draggable = value

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

    