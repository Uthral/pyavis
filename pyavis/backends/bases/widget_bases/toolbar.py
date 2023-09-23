from typing import Callable, Any, List
from .widget import Widget
from pyavis.shared.util.subject import Subject

class BaseToolbar(Widget):
    def __init__(self, labels: List[str], values: List[str]):
        if len(labels) != len(values):
            raise RuntimeError("labels and values need the same length")
        
        self.labels = labels
        self.values = values

        self.mapping = {}
        for label, value in zip(self.labels, self.values):
            self.mapping[label] = value

    def get_active_value(self):
        pass

    def add_on_active_changed(self, func: Callable):
        pass

    def remove_on_active_changed(self, func: Callable):
        pass
