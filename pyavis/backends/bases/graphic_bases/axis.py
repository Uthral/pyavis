from typing import Callable, Literal, Tuple

class Axis:
    def __init__(self, side: Literal['top', 'bottom', 'left', 'right']):
        self._side = side

    def set_disp_func(self, func: Callable[[float], str]):
        '''
        Set the display function, that converts between axis value and axis display text.

        Parameters
        ----------
        func : (float) -> str
            Convert axis value to axis display text
        '''

    def tick_spacing(self, spacing: Tuple[float, float]=None):
        '''
        Set distance of minor and major ticks.

        Paramters
        ---------
        spacing : (float, float) | None, default: None
            Set the spacing between ticks. Format: (major, minor).
            If None, uses default configuration of backend.
        '''

    def toggle_visibility(self, show: bool = True):
        '''
        Show or hide the axis.

        Parameters
        ----------
        show: bool
            To show or hide axis
        '''


