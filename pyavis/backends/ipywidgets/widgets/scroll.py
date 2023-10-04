from pyavis.backends.bases.widget_bases import BaseScrollArea, Widget
from ipywidgets import HBox, Layout

class ScrollAreaIPY(BaseScrollArea):
    def __init__(self, height: int = 100, width: int = 100):
        self.scroll = None
        self.height = height
        self.width = width

    def get_native_widget(self):
        return self.scroll

    def set_widget(self, widget: Widget):
        self.scroll = HBox([widget.get_native_widget()], layout=Layout(width=f'{self.width}px', height=f'{self.height}px', overflow='scroll', display='inline-block'))