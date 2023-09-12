from abc import ABC, abstractmethod

from pyavis.shared.util import Subject
from .track import Track

class Layout(ABC):
    def __init__(self, rows: int = 1, columns: int = 1):
        self.trackAdded = Subject()
        self.trackRemoved = Subject()
        self.tracks = []

        self._rows = rows
        self._columns = columns
    
    @abstractmethod
    def add_track(self, track: Track, row: int, column: int, rowspan: int = 1, colspan: int = 1):
        pass

    @abstractmethod
    def remove_track(self, track):
        pass