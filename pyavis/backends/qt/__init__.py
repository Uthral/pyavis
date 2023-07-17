from .. import _Backend
from .multi_track import MultiTrackVisualizerQt
from .widgets import ButtonQt, DropDownQt, FloatSliderQt, IntSliderQt, VBoxQt, HBoxQt

class _BackendQt(_Backend):
    MultiTrackVisualizer = MultiTrackVisualizerQt
    Button = ButtonQt
    VBox = VBoxQt
    HBox = HBoxQt
    IntSlider = IntSliderQt
    FloatSlider = FloatSliderQt
    DropDown = DropDownQt
