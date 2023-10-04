
from pyavis.backends.bases.widget_bases import BaseGraphicDisp

import pyqtgraph as pg

class GraphicDispQt(BaseGraphicDisp):
    def __init__(self):
        self.widget = pg.GraphicsLayoutWidget()
        self.set_display = None
    
    def set_displayed_item(self, item):
        if self.set_display is not None:
            self.widget.removeItem(self.set_display)
        self.set_display = item
        self.widget.addItem(self.set_display)

    def get_native_widget(self):
        return self.widget