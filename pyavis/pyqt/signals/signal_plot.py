import pyqtgraph as pg

from .signal_renderer import SignalRenderer
from ..axis import createAxis

# TODO: This will be the foundation for the celemony functionality, i.e., movable signals | segmented signal
#       -> use ROI for moving / stretching / deleting? + update
#       -> y axis independent? Pitch on y axis? 

class SignalPlot(pg.GraphicsLayoutWidget):
    def __init__(self, *args, **kwargs):
        super(SignalPlot, self).__init__(*args, **kwargs)
        self.signals: list[SignalRenderer] = []

        self.plotItem = pg.PlotItem()
        self.addItem(self.plotItem)

        for signal in self.signals:
            self._add_to_plot(signal)
        
        axis = createAxis("time", sampling_rate=44100, orientation="bottom")
        self.plotItem.setAxisItems(axisItems={"bottom" : axis})

    def add_signal(self, signal: SignalRenderer):
        self.signals.append(signal)
        self._add_to_plot(signal)

    def _add_to_plot(self, signal: SignalRenderer):
        view = self.plotItem.getViewBox()

        signal.setDraggable(True)
        signal.setClickable(True)
        signal.sigDragged.connect(lambda a,b: signal.update_start(int(b.pos().x())))

        view.addItem(signal)


