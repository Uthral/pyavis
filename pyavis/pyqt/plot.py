import numpy as np
from PySide2 import QtWidgets, QtCore
import pyqtgraph as pg
import pya

from .signal_render import SignalRender
from .time_axis import TimeAxisItem

from pyqtgraph.GraphicsScene.mouseEvents import *

class AudioPlot(QtWidgets.QVBoxLayout):
    def __init__(self, audio: pya.Asig, parent=None):
        super(AudioPlot, self).__init__(parent)
        self.audio = audio

        # TODO: Cleanup drag / select 
        self.drag = True
        self.selection = None

        # TODO: Seperate plot and play button
        self.play_button = QtWidgets.QPushButton("Play")
        self.stop_button = QtWidgets.QPushButton("Stop")

        self.drag_button = QtWidgets.QPushButton("Drag")
        self.select_button = QtWidgets.QPushButton("Select")

        self.plot_widget = pg.GraphicsLayoutWidget()
        self.plot_item = pg.PlotItem()
        self.update_line = UpdateLine(start=0, end=audio.samples, sampling_rate=audio.sr)

        self.plot_widget.addItem(self.plot_item)
        
        divider = pg.InfiniteLine(angle=0, pos=0, pen=pg.mkPen(color='r'))
        self.plot = SignalRender(audio)
        axis_bottom = TimeAxisItem(audio.sr, orientation="bottom")
        
        view = self.plot_item.getViewBox()
        self._calculateViewLimits()
        view.addItem(divider)
        view.addItem(self.plot)
        view.addItem(self.update_line)
        

        self.plot_item.setAxisItems(axisItems={"bottom":axis_bottom})

        self.plot.sigClicked.connect(self._onSignalClick)
        self.plot.sigDragged.connect(self._onSignalDrag)

        hori1 = QtWidgets.QHBoxLayout()
        hori1.addWidget(self.drag_button)
        hori1.addWidget(self.select_button)

        hori2 = QtWidgets.QHBoxLayout()
        hori2.addWidget(self.play_button)
        hori2.addWidget(self.stop_button)

        self.addLayout(hori1)
        self.addLayout(hori2)
        self.addWidget(self.plot_widget)

        self.plot.setClickable(False)
        self.plot.setDraggable(False)

        self.drag_button.clicked.connect(self._toggleDrag)
        self.select_button.clicked.connect(self._toggleSelect)

        self.play_button.clicked.connect(self._onPlayClicked)
        self.stop_button.clicked.connect(self._onStopClicked)



    def _onPlayClicked(self):
        if hasattr(self, 'selection') and self.selection != None:
            (l,r) = self.selection.getRegion()
        else:
            (l,r) = 0, self.audio.samples

        self.update_line.update_positions(l, r)
        self.update_line.start()
        self.audio[int(l):int(r)].play()

    def _onStopClicked(self):
        server = pya.Aserver.default
        self.update_line.stop()
        server.stop()


    # TODO: Cleanup
    def _toggleDrag(self):
        if self.drag == False:
            self.drag = True
            self.plot.setClickable(False)
            self.plot.setDraggable(False)
    
    # TODO: Cleanup
    def _toggleSelect(self):
        if self.drag == True:
            self.drag = False
            self.plot.setClickable(True)
            self.plot.setDraggable(True)

    def _calculateViewLimits(self, padding: float = 0.1):
        """ 
        Calculate the limits of the :class:`ViewBox <pyqtgraph.ViewBox>` of the display based
        on the audio data.

        Parameters
        ----------
        padding : float, default: 0.1
            Padding added to y-Axis
        """
        xMin = 0
        xMax = self.audio.samples
        yMin = np.min(self.audio.sig) - padding
        yMax = np.max(self.audio.sig) + padding 
        yRange = np.abs(yMax) + np.abs(yMin)

        view_box = self.plot_item.getViewBox()
        view_box.setLimits(xMin=xMin, xMax=xMax, yMin=yMin, yMax=yMax, minYRange=yRange, maxYRange=yRange) 

    def _onSignalClick(self, render: SignalRender, event: MouseClickEvent):
        if self.selection:
            view = self.plot_item.getViewBox()
            view.removeItem(self.selection)
            self.selection = None
        pass

    def _onSignalDrag(self, render: SignalRender, event: MouseDragEvent):
        if not self.selection:
            self.selection = pg.LinearRegionItem(values=(event.pos().x(), event.pos().x()), orientation=pg.LinearRegionItem.Vertical)
            self.start_pos = event.pos()

            view = self.plot_item.getViewBox()
            view.addItem(self.selection)
        else:
            self.selection.setRegion((self.start_pos.x(), event.pos().x()))
        pass

    
class UpdateLine(pg.InfiniteLine):
    sigStarted = QtCore.Signal(object)
    sigStopped = QtCore.Signal(object)

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
        self.sigStarted.emit(self)
    
    def stop(self):
        self.timer.stop()
        self.setPos(self.start_pos)
        self.sigStopped.emit(self)

    def update_positions(self, start, end):
        self.start_pos = start
        self.end_pos = end

    def _update_line(self):
        old_pos = self.pos()
        new_pos = old_pos.toQPoint().x() + 0.016 * self.sampling_rate
        
        if new_pos > self.end_pos:
            self.setPos(self.end_pos)
            self.timer.stop()
        else:
            self.setPos(new_pos)