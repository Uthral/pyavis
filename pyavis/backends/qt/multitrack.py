from ...base_classes import AbstractMultiTrackVisualizer

import pyqtgraph as pg

class MultiTrackVisualizerQt(pg.GraphicsLayoutWidget, AbstractMultiTrackVisualizer):
    pass

class _MultiTrack(pg.GraphicsObject):
    pass

class _Track(pg.GraphicsObject):
    pass

class _Signal(pg.GraphicsObject):
    pass