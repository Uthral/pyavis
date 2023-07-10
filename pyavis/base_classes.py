"""
Abstract base classes that implement the shared functionality between
different backends.
"""
from abc import ABC, abstractmethod

class AbstractMultiTrackVisualizer(ABC):
    @abstractmethod
    def get_native_widget(self):
        pass

# class SpectrumVisualizer(ABC):
#     @abstractmethod
#     def get_native_widget(self):
#         pass

# class MelodyneVisualizer(ABC):
#     @abstractmethod
#     def get_native_widget(self):
#         pass

class AbstractButton(ABC):
    @abstractmethod
    def get_native_widget(self):
        pass