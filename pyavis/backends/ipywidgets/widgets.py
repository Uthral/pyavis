from typing import Callable
from overrides import override
from ...base_classes import AbstractButton, AbstractVBox, Widget, AbstractHBox
from ipywidgets import Button, VBox, HBox

class ButtonIPY(AbstractButton):
    def __init__(self, label: str, onClick: Callable):
        self.button = Button(description=label)
        self.button.on_click(lambda _: onClick())
    
    @override
    def get_native_widget(self):
        return self.button

class VBoxIPY(AbstractVBox):
    def __init__(self, *args, **kwargs):
        self.vbox = VBox()
    
    @override
    def add_widget(self, widget: Widget):
        self.vbox.children += (widget.get_native_widget(),)

    @override
    def remove_widget(self, widget: Widget):
        children = list(self.vbox.children)
        children.remove(widget.get_native_widget())
        self.vbox.children = tuple(children)

    @override
    def get_native_widget(self):
        return self.vbox
    
class HBoxIPY(AbstractVBox):
    def __init__(self, *args, **kwargs):
        self.hbox = HBox()
    
    @override
    def add_widget(self, widget: Widget):
        self.hbox.children += (widget.get_native_widget(),)

    @override
    def remove_widget(self, widget: Widget):
        children = list(self.hbox.children)
        children.remove(widget.get_native_widget())
        self.hbox.children = tuple(children)

    @override
    def get_native_widget(self):
        return self.hbox