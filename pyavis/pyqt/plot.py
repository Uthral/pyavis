import numpy as np
from PySide2 import QtWidgets
import pyqtgraph as pg
import pya

class AudioPlot(QtWidgets.QVBoxLayout):
    def __init__(self, audio: pya.Asig, parent=None):
        super(AudioPlot, self).__init__(parent)
        self.audio = audio
        self.play_button = QtWidgets.QPushButton("Play")
        self.plot_item = pg.PlotItem()
        self.plot_widget = pg.GraphicsLayoutWidget()

        self.plot_widget.addItem(self.plot_item)
        
        divider = pg.InfiniteLine(angle=0,pos=0,pen=pg.mkPen(color='b'))
        plot = pg.PlotDataItem(y=audio.sig)
        axis_bottom = TimeAxisItem(audio.sr, orientation="bottom")
        
        self.plot_item.addItem(divider)
        self.plot_item.addItem(plot)
        self.plot_item.setAxisItems(axisItems={"bottom":axis_bottom})

        self.addWidget(self.play_button)
        self.addWidget(self.plot_widget)

class TimeAxisItem(pg.AxisItem):
    def __init__(self, sampling_rate, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)
        self.sampling_rate = sampling_rate
        # self.setTickSpacing(sampling_rate / 4, sampling_rate / 8)

    def tickStrings(self, values, scale, spacing):
        return [f'{value / self.sampling_rate:.2f}' for value in values]