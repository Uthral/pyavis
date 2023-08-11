from ..base_classes import BaseButton, BaseDropDown, BaseFloatSlider, BaseHBox, BaseIntSlider, BaseMultiTrack, BaseScrollArea, BaseSpectrogram, BaseVBox

class _Backend:
    MultiTrack: BaseMultiTrack = None
    SpectroGram: BaseSpectrogram = None
    Button: BaseButton = None
    VBox: BaseVBox = None
    HBox: BaseHBox = None
    IntSlider: BaseIntSlider = None
    FloatSlider: BaseFloatSlider = None
    DropDown: BaseDropDown = None
    ScrollArea: BaseScrollArea = None
    
