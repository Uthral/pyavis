from typing import List, Literal
from overrides import override

import pyqtgraph as pg
import numpy as np

from pyavis.backends.bases.graphic_bases import MultiTrack, Track

from ..graphics.track import TrackQt

class M_MultiTrackQt(type(MultiTrack), type(pg.GraphicsLayoutWidget)): pass
class MultiTrackQt(MultiTrack, pg.GraphicsLayoutWidget, metaclass=M_MultiTrackQt):
    def __init__(self):
        MultiTrack.__init__(self)
        pg.GraphicsLayoutWidget.__init__(self)

        self.tracks: List[TrackQt] = []

        self.track_height: int = 100
        self.mode: Literal["pan","select"] = "pan"

    @override
    def add_track(self, label: str, sampling_rate: int, **kwargs) -> Track:
        track = TrackQt(label, sampling_rate)
        self.addItem(track, col=0)
        self.nextRow()

        self.tracks.append(track)
        self.trackAdded.emit(self, track)

        return track

    @override
    def remove_track(self, identifier: int | str | Track):
        if isinstance(identifier, Track):
            idx = self.tracks.index(identifier)
        elif isinstance(identifier, str):
            track = next(filter(lambda item: item.label == identifier, self.tracks), None)
            idx = self.tracks.index(track)
        elif isinstance(identifier, int):
            idx = identifier
        else:
            raise TypeError("Not a valid type.")
        
        to_remove = self.tracks.pop(idx)
        self.removeItem(to_remove)
        self.trackRemoved.emit(self, to_remove)

    @override
    def update_track_height(self, track_height: int):
        pass

    @override
    def __getitem__(self, index):
        pass

    def get_native_widget(self):
        return self