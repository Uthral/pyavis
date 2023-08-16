"""
Abstract base classes that implement the shared functionality between
different backends.
"""
from abc import ABC, abstractmethod
from typing import Callable, List, Any, Tuple
import numpy as np

from pya import Asig, Astft
from .. import Widget



class BaseTrack(ABC):

    @abstractmethod
    def add_signal(self, position: int, signal, **kwargs):
        pass

    @abstractmethod
    def remove_signal(self, signal):
        pass

    @abstractmethod
    def remove_at_position(self, position: int):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

class BaseSelection(ABC):
    @abstractmethod
    def __init__(self, indices: List[int], start: int, end: int, **kwargs):
        pass
    
    @abstractmethod
    def add_index(self, index: int):
        pass

    @abstractmethod
    def remove_index(self, index: int):
        pass

    @abstractmethod
    def update_region(self, region: Tuple[int, int]):
        pass

class BaseMultiTrack(Widget):
    @abstractmethod
    def add_selection(self, indices: List[int], start: int, end: int) -> BaseSelection:
        pass
    
    @abstractmethod
    def remove_selection(self, selection: BaseSelection):
        pass

    @abstractmethod
    def add_track(self, label: str, sampling_rate: int, **kwargs) -> BaseTrack:
        pass

    @abstractmethod
    def remove_track(self, identifier: int | str | BaseTrack):
        pass

    @abstractmethod
    def update_track_height(self, track_height: int):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

class BaseSpectrogram(Widget):

    @abstractmethod
    def __init__(self, x: Asig | Astft, disp_func: Callable[[np.ndarray], np.ndarray] = np.abs, *args, **kwargs):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def as_asig(self, **kwargs) -> Asig:
        pass

    @abstractmethod
    def as_astft(self) -> Astft:
        pass

    @abstractmethod
    def draw(self, freq: float, time: float):
        pass












