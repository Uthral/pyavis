from overrides import override
from typing import List, Tuple

from ...shared.util import Subject
from ...base_classes import AbstractMultiTrackVisualizer, Selection
from ...shared import AudioSignal
from ...shared.multitrack import MultiTrack, Track

from pyqtgraph.Qt import QtWidgets, QtCore
from pyqtgraph.GraphicsScene.mouseEvents import *
import pyqtgraph as pg
import numpy as np

class MultiTrackVisualizerQt(AbstractMultiTrackVisualizer):
    def __init__(self, multi_track: MultiTrack, *args, **kwargs):
        self.widget = pg.GraphicsLayoutWidget(**kwargs) 
        self.track_renderes: List[_Track] = []
        self.selections: List[SelectionQt] = []
        self.multi_track = multi_track
        
        self.pannZoom = False
        self.selecting = True
        

        top_axis = pg.AxisItem("top")
        self.widget.addItem(item=top_axis, row=0, col=1)
        self.widget.nextRow()

        self.start_pos = None

        top_track_view = None
        for track in multi_track.tracks:
            trk = _Track(track)
            self.track_renderes.append(trk)
            
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
            
            trk.sigDragged.connect(self._selection_track_drag)
            trk.sigHovered.connect(self._selection_track_hover)

            track_axis = pg.AxisItem("left")
            track_axis.linkToView(trk.getViewBox())

            self.widget.addItem(item=track_axis, col=0)
            self.widget.addItem(item=trk, col=1)
            self.widget.nextRow()

    def set_pann_and_zoom(self):
        if self.pannZoom is False:
            self.pannZoom = True
            self.selecting = False

    def set_selecting(self):
        if self.selecting is False:
            self.pannZoom = False
            self.selecting = True

    def _selection_track_drag(self, track, event: MouseDragEvent):
        if not self.selecting:
            return

        if event.isStart():
            self.start_pos = track.getViewBox().mapToView(event.pos())
            self.start_index = self.track_renderes.index(track)
            self.hover_index = self.start_index

            self.active_selection: SelectionQt = self.add_selection(
                [self.start_index], 
                int(self.start_pos.x()), 
                int(self.start_pos.x())
            )

        elif event.isFinish():
            del self.start_pos
            del self.active_selection
        else:
            new_pos = track.getViewBox().mapToView(event.pos())
            self.active_selection.update_region((int(self.start_pos.x()), int(new_pos.x())))
    
    def _selection_track_hover(self, track, event: HoverEvent):
        if not self.selecting: 
            return

        if hasattr(self, 'active_selection'):
            index = self.track_renderes.index(track)

            # TODO: Add / Remove all indecies inbetween (i.e. going from 1 to 3 -> add 2 and 3)
            if index > self.start_index:
                if index > self.hover_index:
                    self.hover_index = index
                    self.active_selection.add_index(self.hover_index)
                else:
                    self.hover_index = index
                    self.active_selection.remove_index(self.hover_index + 1)
            elif index < self.start_index:
                if index < self.hover_index:
                    self.hover_index = index
                    self.active_selection.add_index(self.hover_index)
                else:
                    self.hover_index = index
                    self.active_selection.remove_index(self.hover_index - 1)
            else:
                self.hover_index = self.start_index
                self.active_selection.update_indices([self.start_index])

    
    def get_native_widget(self: bool):
        return self.widget
    
    @override
    def add_selection(self, indices: List[int], start: int, end: int) -> Selection:
        """
        Add a selection over one or multiple tracks

        Parameters
        ----------
        start: int
            Start value in samples
        end: int
            End value in samples
        index: int
            Designates what tracks should be selected
        """
        selection = SelectionQt(indices, start, end)
        selection.selectionAdded.connect(self._on_selection_index_added)
        selection.selectionRemoved.connect(self._on_selection_index_removed)
        selection.selectionsUpdated.connect(self._on_selection_updated)

        for sel in selection.selections:
            self.track_renderes[sel.track_index].addItem(sel)

        self.selections.append(selection)
        return selection

    @override
    def remove_selection(self, selection: Selection):
        selection: SelectionQt = self.selections.pop(self.selections.index(selection))
        selection.selectionAdded.disconnect(self._on_selection_index_added)
        selection.selectionRemoved.disconnect(self._on_selection_index_removed)
        selection.selectionsUpdated.disconnect(self._on_selection_updated)

        for sel in selection.selections:
            self.track_renderes[sel.track_index].removeItem(sel)

        

    def _on_selection_updated(self, arguments):
        old = arguments[0]
        for selection in old:
            self.track_renderes[selection.track_index].removeItem(selection)
        
        new = arguments[1]
        for selection in new:
            self.track_renderes[selection.track_index].addItem(selection)
        
    def _on_selection_index_added(self, arguments):
        selection = arguments[0]
        self.track_renderes[selection.track_index].addItem(selection)

    def _on_selection_index_removed(self, arguments):
        selection = arguments[0]
        self.track_renderes[selection.track_index].removeItem(selection)


# TODO: Extract to use for backend
class SelectionQt(Selection):
    def __init__(self, indices: List[int], start: int, end: int, **kwargs):
        self.selections: List[_Selection] = []
        self.indices: List[int] = []
        self.region = (start, end)

        self.selectionsUpdated = Subject()
        self.selectionAdded = Subject()
        self.selectionRemoved = Subject()

        for index in indices:
            self.add_index(index)

    def update_region(self, region: Tuple[int, int]):
        self.region = region
        for selection in self.selections:
            selection.setRegion(self.region)

    def add_index(self, index: int):
        if index in self.indices:
            return

        selection = _Selection(index, orientation="vertical")
        selection.setRegion(self.region)
        selection.sigRegionChanged.connect(lambda selection: self.update_region(selection.getRegion()))

        self.indices.append(index)
        self.selections.append(selection)
        self.selectionAdded.emit(selection)

    def remove_index(self, index: int):
        if index not in self.indices:
            return
        
        to_remove = next(filter(lambda item: item.track_index == index, self.selections), None)
        to_remove.sigRegionChanged.disconnect()

        self.selections.remove(to_remove)
        self.indices.remove(index)
        self.selectionRemoved.emit(to_remove)

class _Selection(pg.LinearRegionItem):
    def __init__(self, track_index: int, *args, **kwargs):
        # TODO: Allow str, slice, int, ... for indexing
        super(_Selection, self).__init__(**kwargs)
        self.track_index = track_index
        


class _Track(pg.PlotItem):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(self, track: Track, *args, **kwargs):
        super(_Track, self).__init__(*args)
        self.signal_renderers: list[_Signal] = []
        self.track = track

        self.clickable = False
        self.draggable = True

        self._calculateViewLimits()
        self._addMiddleLine()

        for (pos, signal) in track.signals:
            self._addSignal(pos, signal)

        # self.track.onSignalAdded.connect(lambda track, pos, sig: self._addSignal(pos, sig))
        # self.track.onSignalRemoved.connect(lambda track, pos, sig: self._removeSignal(sig))
        # self.track.onSignalMoved.connect(lambda track, pos, sig: self._moveSignal(pos, sig))

        # self.track.onSelectionAdded.connect(lambda arguments: self._selectionAdded(arguments[1], arguments[2]))
        # self.track.onSelectionUpdated.connect(lambda arguments: self._selectionUpdated(arguments[1], arguments[2]))
        # self.track.onSelectionRemoved.connect(lambda arguments: self._selectionRemoved())

    def _addSignal(self, pos: int, signal: AudioSignal):
        viewBox = self.getViewBox()
        sig = _Signal(pos, signal)
        viewBox.addItem(sig)
        self.signal_renderers.append(sig)
    
    def _removeSignal(self, signal: AudioSignal):
        signal_renderer = next(filter(lambda item: item.signal == signal, self.signal_renderers), None)
        self.signal_renderers.remove(signal_renderer)
        viewBox = self.getViewBox()
        viewBox.removeItem(signal_renderer)

    def _moveSignal(self, pos: int, signal: AudioSignal):
        signal_renderer = next(filter(lambda item: item.signal == signal, self.signal_renderers), None)
        signal_renderer.updatePosition(pos)

    def _selectionAdded(self, start: int, end: int):
        self.selection = pg.LinearRegionItem(values=(start, end), orientation=pg.LinearRegionItem.Vertical)
        viewBox = self.getViewBox()
        viewBox.addItem(self.selection)

    def _selectionUpdated(self, start: int, end: int):
        self.selection.setRegion((start, end))

    def _selectionRemoved(self):
        self.getViewBox().removeItem(self.selection)
        self.selection = None

    def _addMiddleLine(self, color="r"):
        """
        Add an horizontal :class:`InfiniteLine <pyqtgraph.InfiniteLine>` to the track, seperating positive and negative numbers.

        Parameters
        ----------
        color : any
            Forwarded to :func:`mkColor <pyqtgraph.mkColor>`
        """
        line = pg.InfiniteLine(angle=0, pos=0, pen=pg.mkPen(color='r'))
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

        view_box = self.getViewBox()
        view_box.setLimits(xMin=xMin, yMin=yMin, yMax=yMax, minYRange=yRange, maxYRange=yRange) 

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

    