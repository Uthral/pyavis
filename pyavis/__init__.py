from . import shared


from .backends import _Backend
from .base_classes import AbstractButton, AbstractFloatSlider, AbstractHBox, AbstractIntSlider, AbstractMultiTrackVisualizer, AbstractDropDown, AbstractVBox

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

def create_multitrack(*args, **kwargs) -> AbstractMultiTrackVisualizer:
    return _get_implementation('MultiTrackVisualizer')(*args, **kwargs)

def create_button(*args, **kwargs) -> AbstractButton:
    return _get_implementation('Button')(*args, **kwargs)

def create_vbox(*args, **kwargs) -> AbstractVBox:
    return _get_implementation('VBox')(*args, **kwargs)

def create_hbox(*args, **kwargs) -> AbstractHBox:
    return _get_implementation('HBox')(*args, **kwargs)

def create_int_slider(*args, **kwargs) -> AbstractIntSlider:
    return _get_implementation('IntSlider')(*args, **kwargs)

def create_float_slider(*args, **kwargs) -> AbstractFloatSlider:
    return _get_implementation('FloatSlider')(*args, **kwargs)

def create_drop_down(*args, **kwargs) -> AbstractDropDown:
    return _get_implementation('DropDown')(*args, **kwargs)


    