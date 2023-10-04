from pyqtgraph.Qt import QtWidgets, QtCore

from pyavis.backends.bases.widget_bases import BaseScrollArea, Widget

class ScrollAreaQt(BaseScrollArea):
    def __init__(self, height: int = 100, width: int = 100):
        self.scroll = QtWidgets.QScrollArea()
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.widget)

        self.scroll.setWidget(self.widget)
        self.scroll.setWidgetResizable(True)

        self.scroll.resize(width, height)

    def set_widget(self, widget: Widget):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        w = widget.get_native_widget()
        self.layout.addWidget(w)

    def get_native_widget(self):
        return self.scroll