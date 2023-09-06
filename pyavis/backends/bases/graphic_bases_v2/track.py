from abc import ABC, abstractmethod
from typing import Literal


class Track(ABC):
    def __init__(self, label: str):
        self.label = label

    def add_signal(self) -> None:
        pass

    def add_line(self) -> None:
        pass

    def add_rect(self) -> None:
        pass

    def add_spectrogram(self) -> None:
        pass

    def add_selection(self) -> None:
        pass

    def set_style(self):
        pass
    
    def link_track(self, track: 'Track', axis: Literal["x", "y"]):
        if axis != 'x' and axis !='y':
            raise ValueError("Not a valid axis")
        
        self._link_track(track, axis)
    
    @abstractmethod
    def _link_track(self, track: 'Track', axis: Literal["x", "y"]):
        pass

    def set_axis(self, axis):
        pass