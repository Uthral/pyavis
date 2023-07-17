from ..base_classes import AbstractButton, AbstractDropDown, AbstractFloatSlider, AbstractHBox, AbstractIntSlider, AbstractMultiTrackVisualizer, AbstractVBox

class _Backend:
    MultiTrackVisualizer: AbstractMultiTrackVisualizer = None
    Button: AbstractButton = None
    VBox: AbstractVBox = None
    HBox: AbstractHBox = None
    IntSlider: AbstractIntSlider = None
    FloatSlider: AbstractFloatSlider = None
    DropDown: AbstractDropDown = None
