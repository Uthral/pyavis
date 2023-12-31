import abc
from pyavis.backends import Backend

from .widgets import *
from .graphics import *
from pyavis import _get_application


class QtBackend(Backend):
    _widget_registry = {}
    _gfx_registry = {}
    
    @classmethod
    def _get_registry(backend, registry_name) -> dict:
        if registry_name == backend._gfx_registry_name:
            return backend._gfx_registry
        elif registry_name == backend._widget_registry_name:
            return backend._widget_registry
        else:
            raise ValueError(registry_name, 'Not a valid registry name')

QtBackend.register_gfx('Layout')(LayoutQt)
QtBackend.register_gfx('Track')(TrackQt)

QtBackend.register_widget('Button')(ButtonQt)
QtBackend.register_widget('ToggleButton')(ToggleButtonQt)
QtBackend.register_widget('Toolbar')(ToolbarQt)
QtBackend.register_widget('DropDown')(DropDownQt)
QtBackend.register_widget('FloatSlider')(FloatSliderQt)
QtBackend.register_widget('IntSlider')(IntSliderQt)
QtBackend.register_widget('ScrollArea')(ScrollAreaQt)
QtBackend.register_widget('VBox')(VBoxQt)
QtBackend.register_widget('HBox')(HBoxQt)
QtBackend.register_widget('GraphicDisp')(GraphicDispQt)


def _show_func(self, exec=False):

    w = self.get_native_widget()
    w.show()

    app = _get_application()
    if app is not None and exec:
        app.exec()

for name, widget in QtBackend.get_widget_registry().items():
    widget.show = _show_func
    abc.update_abstractmethods(widget)

        