from typing import Callable, Literal, Tuple

class Axis:
    def __init__(self, side: Literal['top', 'bottom', 'left', 'right']):
        self._side = side

    def set_disp_func(self, func: Callable[[float], str]):
        pass

    def tick_spacing(self, spacing: Tuple[float, float]=None):
        pass

    def toggle_visibility(self, show: bool = True):
        pass


