from typing import Callable, Any, List

from pyavis.backends.bases.widget_bases import BaseToolbar
from ipywidgets import ToggleButtons

class ToolbarIPY(BaseToolbar):
    def __init__(self, labels: List[str], values: List[str]):
        super().__init__(labels, values)

        self.toolbar = ToggleButtons(options=list(zip(labels, values)))
        self.functions = {}

    def get_native_widget(self):
        return self.toolbar

    def get_active_value(self):
        return self.toolbar.value
        
    def add_on_active_changed(self, func: Callable):
        internal_func = lambda x: func(x["new"])
        self.functions[func] = internal_func
        self.toolbar.observe(self.functions[func], "value")

    def remove_on_active_changed(self, func: Callable):
        internal_func = self.functions.pop(func)
        self.toolbar.unobserve(internal_func, "value")