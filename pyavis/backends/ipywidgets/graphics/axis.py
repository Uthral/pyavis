
from typing import Callable, Literal, Tuple
from pyavis.backends.bases.graphic_bases.axis import Axis

from matplotlib import axes, ticker
from matplotlib.axis import XAxis, YAxis

class AxisIPY(Axis):
    def __init__(self, side: Literal['top', 'bottom', 'left', 'right'], axis: XAxis | YAxis):
        Axis.__init__(self, side)
        self.axis = axis
        self.func = None

    def set_disp_func(self, func: Callable[[float], str]):
        self.func = func

        if func is None:
            self.axis.set_major_formatter(ticker.ScalarFormatter())
            self.axis.set_minor_formatter(ticker.ScalarFormatter())
        else:
            self.axis.set_major_formatter(lambda x, pos: self.func(x))
            self.axis.set_minor_formatter(lambda x, pos: self.func(x))

    def tick_spacing(self, spacing: Tuple[float, float]=None):
        if spacing is None:
            self.axis.set_minor_locator(ticker.AutoMinorLocator(None))
            self.axis.set_major_locator(ticker.AutoLocator())
        else:
            self.axis.set_minor_locator(ticker.MultipleLocator(spacing[1]))
            self.axis.set_major_locator(ticker.MultipleLocator(spacing[0]))

    def toggle_visibility(self, show: bool = True):
        self.axis.set_visible(show)