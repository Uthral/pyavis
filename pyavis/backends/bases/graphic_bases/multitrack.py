from abc import ABC, abstractmethod
from .track import Track

from pyavis.shared.util import Subject


class MultiTrack(ABC):
    def __init__(self):
        self.trackAdded = Subject()
        self.trackRemoved = Subject()
        self.tracks = []

    @abstractmethod
    def add_track(self, label: str, sampling_rate: int, **kwargs) -> Track:
        pass

    @abstractmethod
    def remove_track(self, identifier: int | str | Track):
        pass

    @abstractmethod
    def update_track_height(self, track_height: int):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass