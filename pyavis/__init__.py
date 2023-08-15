from pyavis.backends import Backend

_backend: Backend = None
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
        from .backends.qt_v2 import QtBackend
        _backend = QtBackend
    elif new_backend == "ipywidgets":
        from .backends.ipywidgets_v2 import IPYBackend
        _backend = IPYBackend
    else:
        raise ValueError("Invalid backend") 
    
def _get_backend() -> Backend:
    global _backend
    if _backend is None:
        use_backend()
    return _backend