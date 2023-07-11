from typing import Callable
from overrides import override
from ...base_classes import AbstractButton, AbstractVBox, Widget, AbstractHBox
from pyqtgraph.Qt import QtWidgets

class ButtonQt(AbstractButton):
    def __init__(self, label: str, onClick: Callable, ):
        self.button = QtWidgets.QPushButton(text=label)
        self.button.clicked.connect(onClick)
    
    @override
    def get_native_widget(self):
        return self.button

class VBoxQt(AbstractVBox):
    def __init__(self, *args, **kwargs):
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()

        self.widget.setLayout(self.vbox)
    
    @override
    def add_widget(self, widget: Widget):
        self.vbox.addWidget(widget.get_native_widget())

    @override
    def remove_widget(self, widget: Widget):
        self.vbox.removeWidget(widget.get_native_widget())

    @override
    def get_native_widget(self):
        return self.widget
    
class HBoxQt(AbstractVBox):
    def __init__(self, *args, **kwargs):
        self.widget = QtWidgets.QWidget()
        self.hbox = QtWidgets.QHBoxLayout()

        self.widget.setLayout(self.hbox)
    
    @override
    def add_widget(self, widget: Widget):
        self.hbox.addWidget(widget.get_native_widget())

    @override
    def remove_widget(self, widget: Widget):
        self.hbox.removeWidget(widget.get_native_widget())

    @override
    def get_native_widget(self):
        return self.widget