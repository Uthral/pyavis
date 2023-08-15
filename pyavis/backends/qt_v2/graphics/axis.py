from typing import Callable, Tuple
from overrides import override
import pyqtgraph as pg
import numpy as np

from pyavis.backends.graphics import Axis


class M_AxisQt(type(Axis), type(pg.AxisItem)): pass
class AxisQt(Axis, pg.AxisItem, metaclass=M_AxisQt):
    def __init__(self, orientation, func: Callable[[float], str]):
        Axis.__init__(self)
        pg.AxisItem.__init__(self, orientation)

        self.orientation
        self.func = func

    @override
    def set_disp_func(self, func: Callable[[float], str]):
        '''
        Set the display function, that converts between axis value and axis display text.

        Parameters
        ----------
        func : (float) -> str
            Convert axis value to axis display text
        '''
        self.func = func

    @override
    def set_spacing(self, spacing: Tuple[float, float]=None):
        '''
        Set distance of minor and major ticks.

        Paramters
        ---------
        spacing : (float, float) | None, default: None
            Set the spacing between ticks. Format: (major, minor).
            If None, uses default value.
        '''
        if spacing is None:
            self.setTickSpacing()
        else:
            self.setTickSpacing(*spacing)

    @override
    def tickStrings(self, values, scale, spacing):
        return [f'{self.func(value)}' for value in values] 