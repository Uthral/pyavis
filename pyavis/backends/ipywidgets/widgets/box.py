from pyavis.backends.bases.widget_bases import BaseVBox, Widget, BaseHBox
from ipywidgets import VBox, HBox

class VBoxIPY(BaseVBox):
    def __init__(self):
        self.vbox = VBox()
    
    def add_widget(self, widget: Widget):
        self.vbox.children += (widget.get_native_widget(),)

    def remove_widget(self, widget: Widget):
        children = list(self.vbox.children)
        children.remove(widget.get_native_widget())
        self.vbox.children = tuple(children)

    def get_native_widget(self):
        return self.vbox
    
class HBoxIPY(BaseHBox):
    def __init__(self):
        self.hbox = HBox()
    
    def add_widget(self, widget: Widget):
        self.hbox.children += (widget.get_native_widget(),)

    def remove_widget(self, widget: Widget):
        children = list(self.hbox.children)
        children.remove(widget.get_native_widget())
        self.hbox.children = tuple(children)

    def get_native_widget(self):
        return self.hbox