from .widgets import ButtonIPY, HBoxIPY, VBoxIPY
from .. import _Backend

class _BackendIPyWidgets(_Backend):
    MultiTrackVisualizer = None
    Button = ButtonIPY
    VBox = VBoxIPY
    HBox = HBoxIPY