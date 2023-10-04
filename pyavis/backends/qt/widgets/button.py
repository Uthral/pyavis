from typing import Callable, Any
from pyqtgraph.Qt import QtWidgets, QtCore


from pyavis.backends.bases.widget_bases import BaseButton, BaseToggleButton

class ButtonQt(BaseButton):
    def __init__(self, label: str):
        self.button = QtWidgets.QPushButton(text=label)
    
    def get_native_widget(self):
        return self.button
    
    def add_on_click(self, func: Callable):
        self.button.clicked.connect(func)
    
    def remove_on_click(self, func: Callable):
        self.button.clicked.disconnect(func)

class ToggleButtonQt(BaseToggleButton):
    def __init__(self, label: str, icon: Any = None, default_toggle_state: bool = False):
        if icon is not None:
            self.button = QtWidgets.QPushButton(icon=icon, text=label)
        else:
            self.button = QtWidgets.QPushButton(text=label)
        
        self.button.setCheckable(True)
        self.button.setChecked(default_toggle_state)

    def get_native_widget(self):
        return self.button

    def add_on_toggle(self, func: Callable):
        self.button.toggled.connect(func)

    def remove_on_toggle(self, func: Callable):
        self.button.toggled.disconnect(func)