from typing import Callable, Any, List
from overrides import override
from pyqtgraph.Qt import QtWidgets, QtCore

# from PySide2 import QtWidgets, QtCore

from pyavis.backends.bases.widget_bases import BaseToolbar

class ToolbarQt(BaseToolbar):
    def __init__(self, labels: List[str], values: List[str]):
        super().__init__(labels, values)
        self.functions = {}


        self.toolbar_internal = QtWidgets.QButtonGroup()
        self.toolbar_internal.setExclusive(True)

        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout()

        for id, label in enumerate(self.labels):
            button = QtWidgets.QPushButton(text=label)
            button.setCheckable(True)

            self.toolbar_internal.addButton(button, id)
            self.layout.addWidget(button)

        
        self.widget.setLayout(self.layout)

    @override
    def get_native_widget(self):
        return self.widget
    
    def get_active_value(self):
        id = self.toolbar_internal.checkedId()
        if id is None:
            return None
        
        value = self.mapping[self.labels[id]]
        return value
        

    def add_on_active_changed(self, func: Callable):
        internal_func = lambda x, self=self: func(self.mapping[self.labels[self.toolbar_internal.id(x)]])
        self.functions[func] = internal_func
        self.toolbar_internal.buttonClicked.connect(self.functions[func])

    def remove_on_active_changed(self, func: Callable):
        internal_func = self.functions[func]
        self.toolbar_internal.buttonClicked.disconnect(internal_func)