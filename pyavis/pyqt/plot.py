import numpy as np
from PySide2 import QtWidgets, QtCore
import pyqtgraph as pg
import pya

class AudioPlot(QtWidgets.QVBoxLayout):
    def __init__(self, audio: pya.Asig, parent=None):
        super(AudioPlot, self).__init__(parent)
        self.audio = audio

        # TODO: Seperate plot and play button
        self.play_button = QtWidgets.QPushButton("Play")
        self.stop_button = QtWidgets.QPushButton("Stop")

        self.plot_item = pg.PlotItem()
        self.plot_widget = pg.GraphicsLayoutWidget()
        self.update_line = UpdateLine(start=0, end=audio.samples, sampling_rate=audio.sr)

        self.plot_widget.addItem(self.plot_item)
        
        divider = pg.InfiniteLine(angle=0,pos=0,pen=pg.mkPen(color='b'))
        plot = pg.PlotDataItem(y=audio.sig)
        axis_bottom = TimeAxisItem(audio.sr, orientation="bottom")
        
        self.plot_item.addItem(divider)
        self.plot_item.addItem(plot)
        self.plot_item.setAxisItems(axisItems={"bottom":axis_bottom})
        self.plot_item.addItem(self.update_line)

        hori = QtWidgets.QHBoxLayout()
        hori.addWidget(self.play_button)
        hori.addWidget(self.stop_button)

        self.addLayout(hori)
        self.addWidget(self.plot_widget)

        self.play_button.clicked.connect(self._onPlayClicked)
        self.stop_button.clicked.connect(self._onStopClicked)

    def _onPlayClicked(self):
        # TODO: Add manual blocking
        self.update_line.start()
        self.audio.play()
    
    def _onStopClicked(self):
        # TODO: Better way of getting server
        server = pya.Aserver.default
        self.update_line.stop()
        server.stop()

class TimeAxisItem(pg.AxisItem):
    def __init__(self, sampling_rate, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)
        self.sampling_rate = sampling_rate

    def tickStrings(self, values, scale, spacing):
        return [f'{value / self.sampling_rate:.2f}' for value in values]
    
class UpdateLine(pg.InfiniteLine):
    def __init__(self, start, end, sampling_rate, parent=None):
        super(UpdateLine, self).__init__(angle=90, pos=start)
        self.start_pos = start
        self.end_pos = end
        self.sampling_rate = sampling_rate
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update_line)
        
    def start(self):
        self.setPos(self.start_pos)
        self.timer.start(16)
    
    def stop(self):
        self.timer.stop()
        self.setPos(self.start_pos)

    def _update_line(self):
        old_pos = self.pos()
        new_pos = old_pos.toQPoint().x() + 0.016 * self.sampling_rate
        
        print(new_pos)
        if new_pos > self.end_pos:
            self.timer.stop()

        self.setPos(new_pos)