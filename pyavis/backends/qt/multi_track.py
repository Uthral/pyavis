from overrides import override
from typing import List

from ...base_classes import AbstractMultiTrackVisualizer, BaseSelection, BaseTrack
from ...shared.multitrack import Track

from .multitrack import TrackQt, SelectionQt

from pyqtgraph.GraphicsScene.mouseEvents import *
import pyqtgraph as pg
import numpy as np

class MultiTrackVisualizerQt(AbstractMultiTrackVisualizer):
    def __init__(self, *args, **kwargs):
        self.widget = pg.GraphicsLayoutWidget(*args, **kwargs) 
        
        self.pannZoom = False
        self.selecting = False

        self.selections: List[SelectionQt] = []
        self.tracks: List[TrackQt] = []

        self.top_axis = pg.AxisItem("top")
        self.widget.addItem(item=self.top_axis, col=2)
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
            self.start_index = self.tracks.index(track)
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
            index = self.tracks.index(track)

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
    def add_selection(self, indices: List[int], start: int, end: int) -> BaseSelection:
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
            self.tracks[sel.track_index].addItem(sel)

        self.selections.append(selection)
        return selection

    @override
    def remove_selection(self, selection: BaseSelection):
        selection: SelectionQt = self.selections.pop(self.selections.index(selection))
        selection.selectionAdded.disconnect(self._on_selection_index_added)
        selection.selectionRemoved.disconnect(self._on_selection_index_removed)
        selection.selectionsUpdated.disconnect(self._on_selection_updated)

        for sel in selection.selections:
            self.tracks[sel.track_index].removeItem(sel)

    @override
    def add_track(self, label: str, sampling_rate: int, **kwargs) -> BaseTrack:
        track = TrackQt(label, sampling_rate, **kwargs)
        top_track_view = None if len(self.tracks) == 0 else self.tracks[0].getViewBox()

        if top_track_view is not None: 
            track.getViewBox().setXLink(top_track_view)
        else:
            top_track_view = track.getViewBox()
            self.top_axis.linkToView(top_track_view)

        self.tracks.append(track)

        track.hideAxis("bottom")
        track.hideAxis("left")

        track.sigDragged.connect(self._selection_track_drag)
        track.sigHovered.connect(self._selection_track_hover)

        track_axis = pg.AxisItem("left")
        track_axis.linkToView(track.getViewBox())
        
        # TODO: Just use PlotItem functionality
        self.widget.addLabel(track.label, col=0, angle=-90)
        self.widget.addItem(item=track_axis, col=1)
        self.widget.addItem(item=track, col=2)
        self.widget.nextRow()

        return track

    @override
    def remove_track(self, ident: int | str | BaseTrack):
        if isinstance(ident, Track):
            self.tracks.remove(ident)
        elif isinstance(ident, int):
            self.tracks.pop(ident)
        elif isinstance(ident, str):
            result = next(filter(lambda item: item.label == ident, self.tracks), None)
            self.tracks.pop(result)
        else:
            raise TypeError("Not a valid type.")
        
    @override
    def __getitem__(self, index):
        pass

    def _on_selection_updated(self, arguments):
        old = arguments[0]
        for selection in old:
            self.tracks[selection.track_index].removeItem(selection)
        
        new = arguments[1]
        for selection in new:
            self.tracks[selection.track_index].addItem(selection)
        
    def _on_selection_index_added(self, arguments):
        selection = arguments[0]
        self.tracks[selection.track_index].addItem(selection)

    def _on_selection_index_removed(self, arguments):
        selection = arguments[0]
        self.tracks[selection.track_index].removeItem(selection)       

    