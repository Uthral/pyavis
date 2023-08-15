from typing import Tuple, Any, List

from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from pyavis.base_classes import BaseSelection
from pyavis.shared.util import Subject


class SelectionIPY(BaseSelection):
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