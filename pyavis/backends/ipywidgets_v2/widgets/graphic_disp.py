from overrides import override
from pyavis.backends.bases.widget_bases import BaseGraphicDisp

class GraphicDispIPY(BaseGraphicDisp):
    @override
    def __init__(self):
        self.set_display = None

    @override
    def set_displayed_item(self, item):
        self.set_display = item

    @override
    def get_native_widget(self):
        return self.set_display.fig.canvas

