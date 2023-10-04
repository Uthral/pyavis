from pyavis.backends.bases.widget_bases import BaseGraphicDisp

class GraphicDispIPY(BaseGraphicDisp):
    def __init__(self):
        self.set_display = None

    def set_displayed_item(self, item):
        self.set_display = item

    def get_native_widget(self):
        return self.set_display.fig.canvas

