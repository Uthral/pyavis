import numpy as np

from typing import List
from pyavis.shared.multitrack.track import Track

class MultiTrack:
    def __init__(self):
        self.tracks: List[Track] = []

    def get_section(self, start: int, end: int) -> List[np.ndarray]:
        sections = []
        for track in self.tracks:
            sections.append(track.get_section(start, end))

        return sections
    
    def get_track(self, index: int):
        return self.tracks[index]

    def add_track(self, track: Track):
        self.tracks.append(track)
    
    def remove_track(self, track: Track | int) -> Track:
        removed: Track = None
        if isinstance(track, Track):
            self.tracks.remove(track)
            removed = track
        elif isinstance(track, int):
            removed = self.tracks.pop(track)

        return removed
    