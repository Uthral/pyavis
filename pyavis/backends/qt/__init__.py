from .. import _Backend
from .multi_track import MultiTrackVisualizerQt
from .widgets import ButtonQt, VBoxQt, HBoxQt

class _BackendQt(_Backend):
    MultiTrackVisualizer = MultiTrackVisualizerQt
    Button = ButtonQt
    VBox = VBoxQt
    HBox = HBoxQt
