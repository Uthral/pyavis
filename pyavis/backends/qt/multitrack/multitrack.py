from overrides import override
from typing import List

from ....base_classes import AbstractMultiTrackVisualizer, BaseSelection, BaseTrack
from ....shared.multitrack import Track

from . import TrackQt, SelectionQt

from pyqtgraph.GraphicsScene.mouseEvents import *
import pyqtgraph as pg
import numpy as np

class MultiTrackVisualizerQt(AbstractMultiTrackVisualizer):
    def __init__(self, *args, **kwargs):
        self.widget = pg.GraphicsLayoutWidget(*args, **kwargs) 

        self.selections: List[SelectionQt] = []
        self.tracks: List[TrackQt] = []
        self.top_track: TrackQt = None

        self.pannZoom = False
        self.selecting = False
        self.track_height = 100

        self.top_axis = pg.AxisItem("top")

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
        self.widget.addItem(item=track, col=0)
        self.widget.nextRow()

        top_track_view = None if len(self.tracks) == 0 else self.tracks[0].getViewBox()
        if top_track_view is not None: 
            track.getViewBox().setXLink(top_track_view)
        else:
            self.top_track = track
            self.top_track.setAxisItems({"top": self.top_axis})

        self.tracks.append(track)

        track.hideAxis("bottom")
        track.setLabel("left", track.label)        

        track.sigDragged.connect(self._selection_track_drag)
        track.sigHovered.connect(self._selection_track_hover)

        self.update_track_height(self.track_height)

        return track

    @override
    def remove_track(self, identifier: int | str | BaseTrack):
        if isinstance(identifier, BaseTrack):
            idx = self.tracks.index(identifier)
        elif isinstance(identifier, str):
            track = next(filter(lambda item: item.label == identifier, self.tracks), None)
            idx = self.tracks.index(track)
        elif isinstance(identifier, int):
            idx = identifier
        else:
            raise TypeError("Not a valid type.")
        
        to_remove = self.tracks.pop(idx)
        to_remove.sigDragged.disconnect(self._selection_track_drag)
        to_remove.sigHovered.disconnect(self._selection_track_hover)
        self.widget.removeItem(to_remove)

        # Removed the highest track, so we need to replace it with the new highest track or None
        if idx == 0:
            self.top_track = self.tracks[0] if len(self.tracks) > 0 else None
            self.top_track.setAxisItems({"top": self.top_axis})

            for track in self.tracks:
                track.getViewBox().setXLink(self.top_track.getViewBox())

        # Update track height again, since upper axis was added to new track
        self.update_track_height(self.track_height)        
            
    @override
    def update_track_height(self, track_height: int = 100):
        self.track_height = track_height
        
        # Set height of each tracks view.
        # Highest track (PlotItem) 'loses' height through the top axis, adjust accordingly
        for track in self.tracks:
            if track is self.top_track:
                top_height = track_height + self.top_axis.height()
                track.setFixedHeight(top_height)
            else:
                track.setFixedHeight(track_height)

    # TODO: Extract this to a base class
    @override
    def __getitem__(self, index):
        """ Accessing array elements through slicing.
            * int, get signal row asig[4];
            * slice, range and step slicing asig[4:40:2]
                # from 4 to 40 every 2 samples;
            * list, subset rows, asig[[2, 4, 6]]
                # pick out index 2, 4, 6 as a new asig
            * tuple, row and column specific slicing, asig[4:40, 3:5]
                # from 4 to 40, channel 3 and 4
            * Time slicing (unit in seconds) using dict asig[{1:2.5}, :]
                creates indexing of 1s to 2.5s.
            * Channel name slicing: asig['l'] returns channel 'l' as
                a new mono asig. asig[['front', 'rear']], etc...
            * bool, subset channels: asig[:, [True, False]]


        Parameters
        ----------
            index : Number or slice or list or tuple or dict
                Slicing argument.

        Returns
        -------
            a : Asig
                __getitem__ returns a subset of the self based on the slicing.
        """

        if isinstance(index, tuple):
            # value_idx can be a slice or dict
            # track_idx can be a int, str, list[int], list[bool], list[str] or slice
            value_idx: slice | dict = index[0]
            track_idx: int | str | list[int] | list[bool] | list[str] | slice = index[1]
        elif isinstance(index, str):
            # Get channel / track via label
            value_idx: slice = slice(None, None, None)
            track_idx: str = index
        elif isinstance(index, int):
            # Get channel / track via index
            value_idx: slice = slice(None, None, None)
            track_idx: int = index
        elif isinstance(index, list):
            # Get channel / track via list of indices or strings
            value_idx: slice = slice(None, None, None)
            track_idx: List[int] | List[bool] | List[str] = index
        elif isinstance(index, slice):
            # Get all values of all tracks in the slice range
            value_idx: slice = index
            track_idx: slice = slice(None, None, None)
        elif isinstance(index, dict):
            value_idx: dict = index
            track_idx: slice = slice(None, None, None)
        else:
            # Other inputs will be rejected
            raise TypeError("Invalid type argument")
        
        # Convert str, list[str] and list[bool] into int or list[int] to simplifiy the next steps
        if isinstance(track_idx, str):
            track_idx = self.tracks.index(next(filter(lambda item: item.label == track_idx, self.tracks), None))
        elif isinstance(track_idx, list) and isinstance(track_idx[0], str):
            track_idx = [self.tracks.index(next(filter(lambda item: item.label == label, self.tracks), None)) for label in track_idx]
        elif isinstance(track_idx, list) and isinstance(track_idx[0], bool):
            if len(track_idx) != len(self.tracks):
                raise IndexError("boolean index does not match amount of tracks")
            track_idx = [index for (index, boolean) in enumerate(track_idx) if boolean]

        # Covert value_idx of type dict into slice 
        if isinstance(value_idx, dict):
            # TODO: Refactor, so that a multi track has itself a sampling rate
            sampling_rate = self.tracks[0].sampling_rate
            for key, val in value_idx.items():
                try:
                    start = int(key * sampling_rate)
                except TypeError: 
                    start = None
                try:
                    stop = int(val * sampling_rate)
                except TypeError:
                    stop = None
            value_idx = slice(start, stop, 1)

        # From here on value_idx will always be slice
        # track_idx will be an int, list[int] or slice
        if isinstance(track_idx, int):
            values = self.tracks[track_idx].track[value_idx]
        elif isinstance(track_idx, list):
            # TODO: Pad arrays if not of equal length
            values = [self.tracks[idx].track[value_idx] for idx in track_idx]
        elif isinstance(track_idx, slice):
            # TODO: Pad arrays if not of equal length
            values = [track.track[value_idx] for track in self.tracks[track_idx]]
        else:
            raise Exception("This should not happen")

        # TODO: Transform into Asig
        return values


        

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