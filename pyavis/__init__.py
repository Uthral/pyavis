from . import shared


from .backends import _Backend
from .base_classes import AbstractButton, AbstractHBox, AbstractMultiTrackVisualizer, AbstractVBox

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
    
def get_backend():
    global _backend
    if _backend is None:
        use_backend()
    return _backend   

def create_multitrack(*args, **kwargs) -> AbstractMultiTrackVisualizer:
    global _backend
    return _backend.MultiTrackVisualizer(*args, **kwargs)

def create_button(*args, **kwargs) -> AbstractButton:
    global _backend
    return _backend.Button(*args, **kwargs)

def create_vbox(*args, **kwargs) -> AbstractVBox:
    global _backend
    return _backend.VBox(*args, **kwargs)

def create_hbox(*args, **kwargs) -> AbstractHBox:
    global _backend
    return _backend.HBox(*args, **kwargs)
    