import abc
from overrides import override

from pyavis.backends import Backend
from .widgets import *
from .graphics_v2 import *

class IPYBackend(Backend):
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
        
IPYBackend.register_gfx('Layout')(LayoutIPY)
IPYBackend.register_gfx('Track')(TrackIPY)

IPYBackend.register_widget('Button')(ButtonIPY)
IPYBackend.register_widget('ToggleButton')(ToggleButtonIPY)
IPYBackend.register_widget('Toolbar')(ToolbarIPY)
IPYBackend.register_widget('DropDown')(DropDownIPY)
IPYBackend.register_widget('FloatSlider')(FloatSliderIPY)
IPYBackend.register_widget('IntSlider')(IntSliderIPY)
IPYBackend.register_widget('ScrollArea')(ScrollAreaIPY)
IPYBackend.register_widget('VBox')(VBoxIPY)
IPYBackend.register_widget('HBox')(HBoxIPY)
IPYBackend.register_widget('GraphicDisp')(GraphicDispIPY)




from IPython.display import display

def _show_func(self):
    w = self.get_native_widget()
    display(w)

for name, widget in IPYBackend.get_widget_registry().items():
    widget.show = _show_func
    abc.update_abstractmethods(widget)