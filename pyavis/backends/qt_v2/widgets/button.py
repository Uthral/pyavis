from typing import Callable
from overrides import override
from pyqtgraph.Qt import QtWidgets, QtCore

from pyavis.backends.bases.widget_bases import BaseButton

class ButtonQt(BaseButton):
    def __init__(self, label: str):
        self.button = QtWidgets.QPushButton(text=label)
    
    @override
    def get_native_widget(self):
        return self.button
    
    @override
    def add_on_click(self, func: Callable):
        self.button.clicked.connect(func)
    
    @override
    def remove_on_click(self, func: Callable):
        self.button.clicked.disconnect(func)