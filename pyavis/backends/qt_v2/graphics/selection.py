
from typing import Tuple
from overrides import override
import pyqtgraph as pg
import numpy as np

from pyavis.backends.graphics import Selection


class M_SelectionQt(type(Selection), type(pg.LinearRegionItem)): pass
class SelectionQt(Selection, pg.LinearRegionItem, metaclass=M_SelectionQt):
    def __init__(self, orientation, region: Tuple[float, float]):
        Selection.__init__(self, orientation, region=region)
        pg.LinearRegionItem.__init__(self, values=region, orientation=orientation)

        self.sigRegionChanged.connect(lambda selection: self.set_region(selection.getRegion()))

    @override
    def set_region(self, region: tuple[float, float]):
        '''
        Set the region the selection occupies.

        Parameters
        ----------
        region : (float, float)
            Region to occupy.
        '''
        self.setRegion(region)
        super().set_region(region)

    @override
    def set_active(self, active: bool):
        super().set_active(active)
        self.setVisible(self._active)