import numpy as np

from typing import List
from .track import Track
from ..util import Subject
from pya import Astft

class MultiTrack:
    def __init__(self):
        self.tracks: List[Track] = []

        self.onTrackAdded = Subject()
        self.onTrackRemoved = Subject()
    
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
        """
    
    def get_track(self, track: Track | str |int) -> Track | None:
        result: Track = None
        if isinstance(track, Track):
            try:
                result = self.tracks[self.tracks.index(track)]
            except:
                result = None
        elif isinstance(track, int):
            try:
                result = self.tracks[track]
            except:
                None
        elif isinstance(track, str):
            result = next(filter(lambda item: item.label == track, self.tracks), None)
        else:
            raise TypeError("Not a valid type.")
        return result

    def add_track(self, track: Track):
        self.tracks.append(track)
        self.onTrackAdded.emit(self, track)
    
    def remove_track(self, track: Track | str | int) -> Track:
        removed: Track = None
        if isinstance(track, Track):
            self.tracks.remove(track)
            removed = track
        elif isinstance(track, int):
            removed = self.tracks.pop(track)
        elif isinstance(track, str):
            result = next(filter(lambda item: item.label == track, self.tracks), None)
            removed = self.tracks.pop(result)
        else:
            raise TypeError("Not a valid type.")
        self.onTrackRemoved(self, removed)
        return removed
    