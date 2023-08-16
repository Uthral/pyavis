from overrides import override
from pyqtgraph.Qt import QtWidgets, QtCore

from pyavis.backends.bases.widget_bases import BaseHBox, BaseVBox, Widget

class VBoxQt(BaseVBox):
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
    
class HBoxQt(BaseHBox):
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