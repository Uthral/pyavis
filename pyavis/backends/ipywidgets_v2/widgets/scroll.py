from overrides import override
from pyavis.backends.bases.widget_bases import BaseScrollArea, Widget
from ipywidgets import HBox, Layout

class ScrollAreaIPY(BaseScrollArea):
    @override
    def __init__(self, height: str = '250px'):
        self.scroll = None
        self.height = height

    @override
    def get_native_widget(self):
        return self.scroll

    @override
    def set_widget(self, widget: Widget):
        self.scroll = HBox([widget.get_native_widget()], layout=Layout(height=self.height, overflow='scroll', display='inline-block'))