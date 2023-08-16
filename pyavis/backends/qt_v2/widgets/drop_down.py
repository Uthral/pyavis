from typing import Callable, List, Any
from overrides import override
from pyqtgraph.Qt import QtWidgets, QtCore

from pyavis.backends.bases.widget_bases import BaseDropDown

class DropDownQt(BaseDropDown):

    @override
    def __init__(self, description: str, options: List[Any], default: Any = None):
        self.text = QtWidgets.QLabel(text=description)
        self.drop_down = QtWidgets.QComboBox()

        for option in options:
            if isinstance(option, str):
                self.drop_down.addItem(option)
            else:
                self.drop_down.addItem(str(option))
        idx = options.index(default) if default is not None else 0
        self.drop_down.setCurrentIndex(idx)


        self.box = QtWidgets.QHBoxLayout()
        self.box.addWidget(self.text)
        self.box.addWidget(self.drop_down)
        
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.box)

    @override
    def get_native_widget(self):
        return self.widget

    @override
    def get_value(self) -> Any | None:
        return self.drop_down.currentData()

    @override
    def add_on_selection_changed(self, func: Callable[[Any], None]):
        self.drop_down.currentIndexChanged.connect(func)

    @override
    def remove_on_selection_changed(self, func: Callable[[Any], None]):
        self.drop_down.currentIndexChanged.disconnect(func)