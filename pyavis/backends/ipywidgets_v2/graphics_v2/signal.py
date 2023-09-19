from overrides import override
from pyavis.backends.bases.graphic_bases_v2.signal import Signal

from matplotlib.axes import Axes


class SignalIPY(Signal):
    def __init__(
            self,
            position,
            vertical_size,
            *args,
            **kwargs
    ):
        if 'ax' not in kwargs:
            raise KeyError("Axes not provided. Cannot instantiate SignalIPY.")
        
        Signal.__init__(self, position, vertical_size, *args, **kwargs)
        self._ax: Axes = kwargs["ax"]
        self._lines, = self._ax.plot(self.x_data + self.position[0], self.y_data_sized + self.position[1])
        self.set_style("default")

    def remove(self):
        self._lines.remove()
        self._lines = None
        self._ax = None

    def _update_plot(self):
        self._lines.set_data((self.x_data + self.position[0], self.y_data_sized + self.position[1]))

    @override
    def _abstract_set_active(self):
        self._lines.set_visible(self.active)
        self._lines.axes.figure.canvas.draw_idle()
    
    @override
    def _abstract_set_data(self):
        self._update_plot()
    
    @override
    def _abstract_set_position(self):
        self._update_plot()
    
    @override
    def _abstract_set_vertical_size(self):
        self._update_plot()

    @override
    def _abstract_set_style(self, line_color):
        from pyavis.shared.util import color
        line_color = color._convert_color(line_color)
        self._lines.set_color(line_color)
