import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from typing import List, Tuple, Any

from overrides import override

from pyavis.base_classes import Selection

from ...shared.util.subject import Subject
from ...shared.multitrack import MultiTrack, Track
from ...base_classes import AbstractMultiTrackVisualizer

class MultiTrackVisualizerIPY(AbstractMultiTrackVisualizer):
    def __init__(self, multi_track: MultiTrack, **kwargs):
        self.figure = plt.figure(**kwargs)
        self.figure.subplots_adjust(hspace=0)

        self.selecting = True
        self.selections: List[Selection] = []
        
        self.multi_track = multi_track
        self.track_renderers: List[_Track] = []

        self.dimensions = len(multi_track.tracks)
        subplots: List[Axes] = self.figure.subplots(self.dimensions, sharex=True, sharey=True, subplot_kw={"axes_class": _Track})

        for index, (track, ax) in enumerate(zip(self.multi_track.tracks, subplots)):
            ax.set_track(index, track)
            

    def get_native_widget(self):
        return self.figure.canvas
    
    @override
    def add_selection(self, indices, start, end) -> Selection:
        selection = SelectionIPY(indices, start, end, fig=self.figure)
        self.selections.append(selection)
        return selection
    
    @override
    def remove_selection(self, selection: Selection):
        self.selections.remove(selection)

    @override
    def add_track(self, label: str, sampling_rate: int, **kwargs):
        pass

    @override
    def remove_track(self, ident: int | str | Track):
        pass


class _Track(Axes):
    def set_track(self, index: int, track: Track):
        self.track_index = index
        self.track = track
        self.set_ylabel(track.label)
        for pos, signal in self.track.signals:
            self.plot(range(pos, pos + len(signal.signal())), signal.signal())


class TrackIPY(Track):
    @override
    def __init__(self, label: str, sampling_rate: int, **kwargs):
        pass

    @override
    def add_signal(self, position: int, signal, **kwargs):
        pass

    @override
    def remove_signal(self, signal):
        pass

    @override
    def remove_at_position(self, position: int):
        pass

    @override
    def __getitem__(self, index):
        pass

class SelectionIPY(Selection):
    def __init__(self, indices: List[int], start: int, end: int, **kwargs):
        self.selections: List[_TrackSelection] = []
        self.indices: List[int] = []
        self.region = (start, end)

        self.fig: Figure = kwargs["fig"]

        self.selectionsUpdated = Subject()
        self.selectionAdded = Subject()
        self.selectionRemoved = Subject()

        for index in indices:
            self.add_index(index)
    
    def update_region(self, region: Tuple[int, int]):
        self.region = region
        for selection in self.selections:
            selection.extents = self.region
    
    def update_indices(self, indices: List[int]):
        pass

    def add_index(self, index: int):
        if index in self.indices:
            return

        selection = _TrackSelection(
            index,
            ax=self.fig.axes[index], 
            onselect=self._on_select,
            onmove_callback=self._on_move, 
            direction="horizontal", 
            interactive=True,
            drag_from_anywhere=True,
            ignore_event_outside=True,
            useblit=True
        )
        self.selections.append(selection)
        selection.extents = self.region
        # https://discourse.matplotlib.org/t/how-do-i-make-multiple-span-selectors-work-on-the-same-axis/23285/5
        selection._selection_completed = True

        self.indices.append(index)
        self.selections.append(selection)
        self.selectionAdded.emit(selection)

    def remove_index(self, index: int):
        if index not in self.indices:
            return
        
        to_remove = next(filter(lambda item: item.track_index == index, self.selections), None)
        
        to_remove.set_visible(False)
        to_remove.active = False
        self.fig.canvas.draw_idle()

        self.selections.remove(to_remove)
        self.indices.remove(index)

    def _update_selections(self, region):
        pass

    def _on_select(self, minVal, maxVal) -> Any:
        pass

    def _on_move(self, minVal, maxVal):
        self.update_region((minVal, maxVal))

class _TrackSelection(SpanSelector):
    def __init__(self, track_index: int, **kwargs):
        super(_TrackSelection, self).__init__(**kwargs)
        self.track_index = track_index



import matplotlib.projections as proj
proj.register_projection(_Track)
