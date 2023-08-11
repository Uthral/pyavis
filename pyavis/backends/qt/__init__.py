import abc


from .. import _Backend
from .multitrack import MultiTrackQt
from .spectrogram import SpectrogramQt
from .widgets import ButtonQt, DropDownQt, FloatSliderQt, IntSliderQt, ScrollAreaQt, VBoxQt, HBoxQt

class _BackendQt(_Backend):
    MultiTrack = MultiTrackQt
    Spectrogram = SpectrogramQt
    Button = ButtonQt
    VBox = VBoxQt
    HBox = HBoxQt
    IntSlider = IntSliderQt
    FloatSlider = FloatSliderQt
    DropDown = DropDownQt
    ScrollArea = ScrollAreaQt

def _show_func(self):
    w = self.get_native_widget()
    w.show()

for attribute in _BackendQt.__dict__.keys():
    # TODO: Replace with list of strings or just implement base class
    if attribute[:2] != '__':
        widget_type = getattr(_BackendQt, attribute)
        widget_type.show = _show_func
        abc.update_abstractmethods(widget_type)