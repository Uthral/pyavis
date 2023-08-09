import abc
from .widgets import ButtonIPY, FloatSliderIPY, HBoxIPY, IntSliderIPY, DropDownIPY, ScrollAreaIPY, VBoxIPY
from .multitrack.multi_track import MultiTrackIPY
from .. import _Backend
from IPython.display import display 

class _BackendIPyWidgets(_Backend):
    MultiTrackVisualizer = MultiTrackIPY
    Button = ButtonIPY
    VBox = VBoxIPY
    HBox = HBoxIPY
    IntSlider = IntSliderIPY
    FloatSlider  = FloatSliderIPY
    DropDown = DropDownIPY
    ScrollArea = ScrollAreaIPY

def _show_func(self):
    w = self.get_native_widget()
    display(w)

for attribute in _BackendIPyWidgets.__dict__.keys():
    # TODO: Replace with list of strings or just implement base class
    if attribute[:2] != '__':
        class_type = getattr(_BackendIPyWidgets, attribute)
        class_type.show = _show_func
        abc.update_abstractmethods(class_type)
