import abc
from overrides import override

from pyavis.backends import Backend
from .graphics import *
from .widgets import *

from .multitrack import MultiTrackQt

class QtBackend(Backend):
    _widget_registry = {}
    _gfx_registry = {}
    
    @classmethod
    @override
    def _get_registry(backend, registry_name) -> dict:
        if registry_name == backend._gfx_registry_name:
            return backend._gfx_registry
        elif registry_name == backend._widget_registry_name:
            return backend._widget_registry
        else:
            raise ValueError(registry_name, 'Not a valid registry name')

QtBackend.register_gfx('Rectangle')(RectangleQt)
QtBackend.register_gfx('Signal')(SignalQt)
QtBackend.register_gfx('Track')(TrackQt)
QtBackend.register_gfx('Axis')(AxisQt)
QtBackend.register_gfx('Selection')(SelectionQt)
QtBackend.register_gfx('MultiTrack')(MultiTrackQt)

QtBackend.register_widget('Button')(ButtonQt)
QtBackend.register_widget('DropDown')(DropDownQt)
QtBackend.register_widget('FloatSlider')(FloatSliderQt)
QtBackend.register_widget('IntSlider')(IntSliderQt)
QtBackend.register_widget('ScrollArea')(ScrollAreaQt)
QtBackend.register_widget('VBox')(VBoxQt)
QtBackend.register_widget('HBox')(HBoxQt)

# Deprecated
from .deprecated import SpectrogramQt as DepSpectrogramQt, MultiTrackQt as DepMultiTrackQt
QtBackend.register_widget('DepMultiTrack')(DepMultiTrackQt)
QtBackend.register_widget('DepSpectrogram')(DepSpectrogramQt)

def _show_func(self):
    w = self.get_native_widget()
    w.show()

for name, widget in QtBackend.get_widget_registry().items():
    widget.show = _show_func
    abc.update_abstractmethods(widget)

        