from ..base_classes import AbstractButton, AbstractDropDown, AbstractFloatSlider, AbstractHBox, AbstractIntSlider, BaseMultiTrack, AbstractVBox

class _Backend:
    MultiTrackVisualizer: BaseMultiTrack = None
    Button: AbstractButton = None
    VBox: AbstractVBox = None
    HBox: AbstractHBox = None
    IntSlider: AbstractIntSlider = None
    FloatSlider: AbstractFloatSlider = None
    DropDown: AbstractDropDown = None
