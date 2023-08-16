from . import _get_backend
from .backends import Backend

def _is_missing_implementation(backend: Backend, widget: str):
    if widget not in backend.get_widget_registry():
        class_name = repr(backend)[7:-1]
        raise RuntimeError(f'{class_name} does not implement {widget}')
    
def _get_implementation(widget: str):
    backend = _get_backend()
    _is_missing_implementation(backend, widget)
    return backend.get_widget_registry()[widget]

from .backends.bases.widget_bases import BaseButton, BaseFloatSlider, BaseHBox, BaseIntSlider, BaseDropDown, BaseScrollArea, BaseVBox

def Button(*args, **kwargs) -> BaseButton:
    return _get_implementation('Button')(*args, **kwargs)

def VBox(*args, **kwargs) -> BaseVBox:
    return _get_implementation('VBox')(*args, **kwargs)

def HBox(*args, **kwargs) -> BaseHBox:
    return _get_implementation('HBox')(*args, **kwargs)

def IntSlider(*args, **kwargs) -> BaseIntSlider:
    return _get_implementation('IntSlider')(*args, **kwargs)

def FloatSlider(*args, **kwargs) -> BaseFloatSlider:
    return _get_implementation('FloatSlider')(*args, **kwargs)

def DropDown(*args, **kwargs) -> BaseDropDown:
    return _get_implementation('DropDown')(*args, **kwargs)

def ScrollArea(*args, **kwargs) -> BaseScrollArea:
    return _get_implementation('ScrollArea')(*args, **kwargs)


# Deprecated
from .backends.bases.deprecated.base_classes import BaseMultiTrack, BaseSpectrogram

def DepMultiTrack(*args, **kwargs) -> BaseMultiTrack:
    return _get_implementation('DepMultiTrack')(*args, **kwargs)

def DepSpectrogram(*args, **kwargs) -> BaseSpectrogram:
    return _get_implementation('DepSpectrogram')(*args, **kwargs)