from typing import Callable, Literal, Tuple

class Axis:
    """
    Base class representing an axis on the side of a plot.
    """
    def __init__(self, side: Literal['top', 'bottom', 'left', 'right']):
        """
        Initalizes an axis.

        Parameters
        ----------
        side : Literal[&#39;top&#39;, &#39;bottom&#39;, &#39;left&#39;, &#39;right&#39;]
            Side of the axis
        """
        self._side = side

    def set_disp_func(self, func: Callable[[float], str]):
        """
        Set the display function, that converts between axis value and axis display text.

        Parameters
        ----------
        func : Callable[[float], str]
            Convert axis value to axis display text
        """

    def tick_spacing(self, spacing: Tuple[float, float]=None):
        """
        Set distance of minor and major ticks.

        Parameters
        ----------
        spacing : Tuple[float, float], optional
            Set the spacing between ticks. Format: (major, minor).
            If None, uses default configuration of backend.
        """

    def toggle_visibility(self, show: bool = True):
        """
        Show or hide the axis.

        Parameters
        ----------
        show : bool, optional
            To show or hide axis, by default True
        """


