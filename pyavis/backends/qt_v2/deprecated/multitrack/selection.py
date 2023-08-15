from overrides import override
from typing import List, Tuple, Any

from pyavis.shared.util import Subject
from pyavis.base_classes import BaseSelection

from pyqtgraph.GraphicsScene.mouseEvents import *

import pyqtgraph as pg
import numpy as np

# TODO: Extract to use for backend
# TODO: Extract to use for backend
class SelectionQt(BaseSelection):
    def __init__(self, indices: List[int], start: int, end: int, **kwargs):
        self.selections: List[_Selection] = []
        self.indices: List[int] = []
        self.region = (start, end)

        self.selectionsUpdated = Subject()
        self.selectionAdded = Subject()
        self.selectionRemoved = Subject()

        for index in indices:
            self.add_index(index)

    @override
    def add_index(self, index: int):
        if index in self.indices:
            return

        selection = _Selection(index, orientation="vertical")
        selection.setRegion(self.region)
        selection.sigRegionChanged.connect(lambda selection: self.update_region(selection.getRegion()))

        self.indices.append(index)
        self.selections.append(selection)
        self.selectionAdded.emit(selection)

    @override
    def remove_index(self, index: int):
        if index not in self.indices:
            return
        
        to_remove = next(filter(lambda item: item.track_index == index, self.selections), None)
        to_remove.sigRegionChanged.disconnect()

        self.selections.remove(to_remove)
        self.indices.remove(index)
        self.selectionRemoved.emit(to_remove)

    @override
    def update_region(self, region: Tuple[int, int]):
        self.region = region
        for selection in self.selections:
            selection.setRegion(self.region)

class _Selection(pg.LinearRegionItem):
    def __init__(self, track_index: int, *args, **kwargs):
        # TODO: Allow str, slice, int, ... for indexing
        super(_Selection, self).__init__(**kwargs)
        self.track_index = track_index