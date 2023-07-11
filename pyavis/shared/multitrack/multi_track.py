import numpy as np

from typing import List
from .track import Track
from ..util import Subject

class MultiTrack:
    def __init__(self):
        self.tracks: List[Track] = []
        self._selection_start = None
        self._selection_end = None

        self.onTrackAdded = Subject()
        self.onTrackRemoved = Subject()

        self.onSelectionAdded = Subject()
        self.onSelectionUpdated = Subject()
        self.onSelectionRemoved = Subject()

    def get_section(self, start: int, end: int) -> List[np.ndarray]:
        sections = []
        for track in self.tracks:
            sections.append(track.get_section(start, end))
        return sections
    
    def set_selection(self, start: int, end: int):
        if self._selection_start is None and self._selection_end is None:
            self._selection_start = start
            self._selection_end = end
            self.onSelectionAdded.emit(self, start, end)
        else:
            self._selection_start = start
            self._selection_end = end
            self.onSelectionUpdated.emit(self, start, end)

        for track in self.tracks:
            track.set_selection(start, end)

    def remove_selection(self):
        if self._selection_end is not None and self._selection_end is not None:
            self._selection_start = None
            self._selection_end = None
            self.onSelectionRemoved.emit(self)
    
    def get_selection(self) -> List[np.ndarray] | None:
        if self._selection_start is None or self._selection_end is None:
            return None
        else:
            return self.get_section(self._selection_start, self._selection_end)
    
    def get_track(self, track: Track | int) -> Track:
        result: Track = None
        if isinstance(track, Track):
            result = self.tracks[self.tracks.index(track)]
        elif isinstance(track, int):
            result = self.tracks[track]
        else:
            raise TypeError("Not a valid type.")
        return result

    def add_track(self, track: Track):
        self.tracks.append(track)
        self.onTrackAdded.emit(self, track)
    
    def remove_track(self, track: Track | int) -> Track:
        removed: Track = None
        if isinstance(track, Track):
            self.tracks.remove(track)
            removed = track
        elif isinstance(track, int):
            removed = self.tracks.pop(track)
        else:
            raise TypeError("Not a valid type.")
        self.onTrackRemoved(self, removed)
        return removed
    