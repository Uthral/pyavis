

from typing import Literal, Tuple

from matplotlib.axes import Axes
from matplotlib.patches import Rectangle as MPLRectangle
from pyavis.backends.bases.graphic_bases_v2.rectangle import Rectangle


class RectangleIPY(Rectangle):
    def __init__(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            width: float = 1.0,
            height: float = 1.0,
            **kwargs
    ):
        if 'ax' not in kwargs:
            raise KeyError("Axes not provided. Cannot instantiate SignalIPY.")
        
        Rectangle.__init__(self, position, width, height)
        self._ax: Axes = kwargs["ax"]
        self._rectangle = self._ax.add_artist(MPLRectangle(self.position, self.rect_width, self.rect_height))

    def _update_plot(self):
        self._rectangle.set(xy=self.position, width=self.rect_width, height=self.rect_height)
        self._rectangle.axes.figure.canvas.draw_idle()

    def _abstract_set_width(self):
        self._update_plot()

    def _abstract_set_height(self):
        self._update_plot()

    def _abstract_set_position(self):
        self._update_plot()

    def _abstract_set_active(self):
        self._rectangle.set_visible(self.active)
        self._rectangle.axes.figure.canvas.draw_idle()


    def set_style(self, style: dict | Literal["default"]):
        pass
        
