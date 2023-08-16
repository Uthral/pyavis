from typing import Callable
from overrides import override
from pyavis.backends.bases.widget_bases import BaseButton
from ipywidgets import Button

class ButtonIPY(BaseButton):
    @override
    def __init__(self, label: str):
        self.button = Button(description=label)
    
    @override
    def get_native_widget(self):
        return self.button

    @override
    def add_on_click(self, func: Callable):
        self.button.on_click(func)
    
    def remove_on_click(self, func: Callable):
        self.button.on_click(func, remove=True)