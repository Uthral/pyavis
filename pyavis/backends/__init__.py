from ..base_classes import BaseButton, BaseDropDown, BaseFloatSlider, BaseHBox, BaseIntSlider, BaseMultiTrack, BaseVBox

class _Backend:
    MultiTrackVisualizer: BaseMultiTrack = None
    Button: BaseButton = None
    VBox: BaseVBox = None
    HBox: BaseHBox = None
    IntSlider: BaseIntSlider = None
    FloatSlider: BaseFloatSlider = None
    DropDown: BaseDropDown = None
    
