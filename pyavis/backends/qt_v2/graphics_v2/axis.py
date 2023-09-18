
from types import MethodType
from typing import Callable, Literal, Tuple
from overrides import override
import pyqtgraph as pg
from pyavis.backends.bases.graphic_bases_v2.axis import Axis


class AxisQt(Axis):
    def __init__(self, side: Literal['top', 'bottom', 'left', 'right'], axis: pg.AxisItem):
        Axis.__init__(self, side)
        
        self.axis = axis
        self.func = None

        self.axis.tickStrings = MethodType(tick_render_func, self)

    def set_disp_func(self, func: Callable[[float], str]):
        self.func = func

    def tick_spacing(self, spacing: Tuple[float, float]=None):
        if spacing is None:
            self.axis.setTickSpacing()
        else:
            self.axis.setTickSpacing(*spacing)
    
    def toggle_visibility(self, show: bool = True):
        if show:
            self.axis.show()
        else:
            self.axis.hide()


from math import ceil, log10

def tick_render_func(self, values, scale, spacing):
    if self.func is not None:
        return [f'{self.func(value)}' for value in values] 

    places = max(0, ceil(-log10(spacing * scale)))
    strings = []
    for v in values:
        vs = v * scale
        if abs(vs) < .001 or abs(vs) >= 10000:
            vstr = "%g" % vs
        else:
            vstr = ("%%0.%df" % places) % vs
        strings.append(vstr)
    return strings