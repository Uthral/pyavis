from .widgets import ButtonIPY, FloatSliderIPY, HBoxIPY, IntSliderIPY, DropDownIPY, VBoxIPY
from .multi_track import MultiTrackVisualizerIPY
from .. import _Backend

class _BackendIPyWidgets(_Backend):
    MultiTrackVisualizer = MultiTrackVisualizerIPY
    Button = ButtonIPY
    VBox = VBoxIPY
    HBox = HBoxIPY
    IntSlider = IntSliderIPY
    FloatSlider  = FloatSliderIPY
    DropDown = DropDownIPY
