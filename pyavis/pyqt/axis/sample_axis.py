import pyqtgraph as pg

class SampleAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super(SampleAxisItem, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [f'{value}' for value in values]