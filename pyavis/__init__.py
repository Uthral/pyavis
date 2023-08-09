from . import shared


from .backends import _Backend
from .base_classes import BaseButton, BaseFloatSlider, BaseHBox, BaseIntSlider, BaseMultiTrack, BaseDropDown, BaseScrollArea, BaseSpectrogram, BaseVBox

_backend: _Backend = None
def use_backend(backend: str = "qt"):
    '''
    Parameters
    ----------
    backend : str
        Either "qt" or "ipywidgets"
    '''
    global _backend
    new_backend = backend.lower()
    if new_backend == "qt":
        from .backends.qt import _BackendQt
        _backend = _BackendQt
    elif new_backend == "ipywidgets":
        from .backends.ipywidgets import _BackendIPyWidgets
        _backend = _BackendIPyWidgets
    else:
        raise ValueError("Invalid backend")
    
def _get_backend():
    global _backend
    if _backend is None:
        use_backend()
    return _backend   

def _is_missing_implementation(backend: _Backend, widget: str):
    if (not hasattr(backend, widget) or getattr(backend, widget) is None):
        class_name = repr(backend)[7:-1]
        raise RuntimeError(f'{class_name} does not implement {widget}')
    
def _get_implementation(widget: str):
    backend = _get_backend()
    _is_missing_implementation(backend, widget)
    return getattr(backend, widget)

def create_multitrack(*args, **kwargs) -> BaseMultiTrack:
    return _get_implementation('MultiTrackVisualizer')(*args, **kwargs)

def create_spectrogram(*args, **kwargs) -> BaseSpectrogram:
    return _get_implementation('SpectrogramVisualizer')(*args, **kwargs)

def create_button(*args, **kwargs) -> BaseButton:
    return _get_implementation('Button')(*args, **kwargs)

def create_vbox(*args, **kwargs) -> BaseVBox:
    return _get_implementation('VBox')(*args, **kwargs)

def create_hbox(*args, **kwargs) -> BaseHBox:
    return _get_implementation('HBox')(*args, **kwargs)

def create_int_slider(description="IntSlider", orientation: str = "horizontal", default: int = 50, min: int = 1, max: int = 100, step: int = 1, *args, **kwargs) -> BaseIntSlider:
    return _get_implementation('IntSlider')(*args, **kwargs)

def create_float_slider(*args, **kwargs) -> BaseFloatSlider:
    return _get_implementation('FloatSlider')(*args, **kwargs)

def create_drop_down(*args, **kwargs) -> BaseDropDown:
    return _get_implementation('DropDown')(*args, **kwargs)

def create_scroll_area(*args, **kwargs) -> BaseScrollArea:
    return _get_implementation('ScrollArea')(*args, **kwargs)


    