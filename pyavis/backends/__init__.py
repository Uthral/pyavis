from ..base_classes import AbstractButton, AbstractHBox, AbstractMultiTrackVisualizer, AbstractVBox

class _Backend:
    MultiTrackVisualizer: AbstractMultiTrackVisualizer = None
    Button: AbstractButton = None
    VBox: AbstractVBox = None
    HBox: AbstractHBox = None
