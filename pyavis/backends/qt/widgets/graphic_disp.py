
from overrides import override
from pyavis.backends.bases.widget_bases import BaseGraphicDisp

import pyqtgraph as pg

class GraphicDispQt(BaseGraphicDisp):
    @override
    def __init__(self):
        self.widget = pg.GraphicsLayoutWidget()
        self.set_display = None
    
    @override
    def set_displayed_item(self, item):
        if self.set_display is not None:
            self.widget.removeItem(self.set_display)
        self.set_display = item
        self.widget.addItem(self.set_display)

    @override
    def get_native_widget(self):
        return self.widget