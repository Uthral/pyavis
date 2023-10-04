from typing import Callable, Any
from pyavis.backends.bases.widget_bases import BaseButton, BaseToggleButton
from ipywidgets import Button, ToggleButton

class ButtonIPY(BaseButton):
    def __init__(self, label: str):
        self.button = Button(description=label)
    
    def get_native_widget(self):
        return self.button

    def add_on_click(self, func: Callable):
        self.button.on_click(func)
    
    def remove_on_click(self, func: Callable):
        self.button.on_click(func, remove=True)

class ToggleButtonIPY(BaseToggleButton):
    def __init__(self, label: str, icon: Any = None, default_toggle_state: bool = False):
        if icon is not None:
            self.button = ToggleButton(description=label, icon=icon, value=default_toggle_state)
        else:
            self.button = ToggleButton(description=label, value=default_toggle_state)
        self.functions = {}

    def get_native_widget(self):
        return self.button

    def add_on_toggle(self, func: Callable):
        internal_func = lambda x: func(x["new"])
        self.functions[func] = internal_func
        self.button.observe(self.functions[func], 'value')

    def remove_on_toggle(self, func: Callable):
        internal_func = self.functions.pop(func)
        self.button.unobserve(internal_func, 'value')


