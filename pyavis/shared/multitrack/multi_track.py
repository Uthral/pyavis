from typing import List
from .track import Track
from ..util import Subject

class MultiTrack:
    def __init__(self):
        self.tracks: List[Track] = []

        self.onTrackAdded = Subject()
        self.onTrackRemoved = Subject()
    
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
        self.onTrackRemoved.emit(self, removed)
        return removed
    
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
            return self.tracks[track_idx][value_idx]
        elif isinstance(track_idx, list):
            tracks: list[Track] = [self.tracks[idx] for idx in track_idx]
        elif isinstance(track_idx, slice):
            tracks: list[Track] = self.tracks[track_idx]
        else:
            raise Exception("This should not happen")

        # Different tracks can have different lengths
        # Calc. max values and apply correct slice
        max_length = max([track.track.get_minimum_length() for track in tracks])

        # Update slice if one of the absolute values is greater than our track length
        if value_idx.start is not None and value_idx.start > max_length:
            max_length = value_idx.start
        if value_idx.stop is not None and value_idx.stop > max_length:
            max_length = value_idx.stop

        (start, stop, step) = value_idx.indices(max_length)
        values = [track[start:stop:step] for track in tracks]     

        # TODO: Transform into Asig
        return values
    