from pyavis.backends import Backend

_backend: Backend = None
_backend_str: str = None

def _get_backend() -> Backend:
    global _backend
    if _backend is None:
        use_backend()
    return _backend

def _get_backend_str() -> str:
    global _backend_str
    if _backend_str is None:
        use_backend()
    return _backend_str

def use_backend(backend: str = "qt"):
    '''
    Parameters
    ----------
    backend : str
        Either "qt" or "ipywidgets"
    '''
    global _backend
    global _backend_str
    new_backend = backend.lower()
    if new_backend == "qt":
        from .backends.qt import QtBackend
        _backend = QtBackend
        _backend_str = "qt"
    elif new_backend == "ipywidgets":
        from .backends.ipywidgets import IPYBackend

        import matplotlib
        matplotlib.pyplot.ioff()

        _backend = IPYBackend
        _backend_str = "ipywidgets"
    else:
        raise ValueError("Invalid backend") 
    

