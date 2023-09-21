

from pyavis.backends.bases.widget_bases.widget import Widget
from pyavis.widgets import HBox, GraphicDisp, Button
from pyavis.graphics import Layout

from pyavis.shared.util.util import spec_to_asig

class SpectrogramEdit(Widget):
    def __init__(self):
        self._signal = None

        self._hb = HBox()
        self._spec_disp = GraphicDisp()
        self._signal_disp = GraphicDisp()

        spec_layout = Layout(1,1)
        signal_layout = Layout(1,1)

        self._spec_track = spec_layout.add_track("Spectrogram", 0, 0)
        self._sig_track = signal_layout.add_track("Signal", 0, 0)

        self._spec_disp.set_displayed_item(spec_layout)
        self._signal_disp.set_displayed_item(signal_layout)

        self._hb.add_widget(self._spec_disp)
        self._hb.add_widget(self._signal_disp)

        self._sig_track.set_axis('bottom', spacing=None, disp_func=lambda value: f'{round(value / 44100, 2)}')


    def set_signal(self, signal):
        self._signal = signal

        if hasattr(self, "_gfx_spec"):
            self._spec_track.remove(self._gfx_spec)
            self._sig_track.remove(self._gfx_sig)

        self._gfx_spec = self._spec_track.add_spectrogram(self._signal)
        self._gfx_sig = self._sig_track.add_signal((0,0), "auto", y=self._signal.sig)

        self._gfx_spec.draggable = True
        self._gfx_spec.clickable = True

        self._gfx_spec.onClick.connect(self._draw_on_spec_finish)
        self._gfx_spec.onDragging.connect(self._draw_on_spec)
        self._gfx_spec.onDraggingFinish.connect(self._draw_on_spec_finish)

    def set_brush(self, values, center):
        self._draw_mode = "set"
        self._values = values
        self._center = center

    def _draw_on_spec(self, args):
        self._gfx_spec.set_brush(self._values, None, self._center, draw_mode="set")
        self._gfx_spec.draw(args[1][1], args[1][0])
        self._gfx_spec.clear_brush()

    def _draw_on_spec_finish(self, args):
        asig = spec_to_asig(self._gfx_spec, True)
        self.set_signal(asig)
        pass


    def get_native_widget(self):
        return self._hb.get_native_widget()

    def show(self):
        self._hb.show()

