import pyqtgraph as pg

class TimeAxisItem(pg.AxisItem):
    def __init__(self, sampling_rate, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)
        self.sampling_rate = sampling_rate

    def tickStrings(self, values, scale, spacing):
        return [f'{value / self.sampling_rate:.2f}' for value in values]