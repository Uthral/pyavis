from .widgets import ButtonIPY, FloatSliderIPY, HBoxIPY, IntSliderIPY, DropDownIPY, VBoxIPY
from .. import _Backend

class _BackendIPyWidgets(_Backend):
    MultiTrackVisualizer = None
    Button = ButtonIPY
    VBox = VBoxIPY
    HBox = HBoxIPY
    IntSlider = IntSliderIPY
    FloatSlider  = FloatSliderIPY
    DropDown = DropDownIPY
