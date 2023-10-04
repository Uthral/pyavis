from pyavis.backends import Backend

_backend: Backend = None
_backend_str: str = None

def _get_backend() -> Backend:
    """
    Return active backend, or initalize default backend.

    Returns
    -------
    Backend
        Active backend
    """
    global _backend
    if _backend is None:
        use_backend()
    return _backend

def _get_backend_str() -> str:
    """
    Return active backend string, or initalize default backend.

    Returns
    -------
    str
        String representation of backend
    """
    global _backend_str
    if _backend_str is None:
        use_backend()
    return _backend_str

def use_backend(backend: str = "qt"):
    """
    Choose the backend to use.

    Parameters
    ----------
    backend : str, optional
        Either "qt" or "ipywidgets", by default "qt"

    Raises
    ------
    ValueError
        Raises if backend is not known
    """
    global _backend
    global _backend_str
    new_backend = backend.lower()
    if new_backend == "qt":
        from .backends.qt import QtBackend
        _backend = QtBackend
        _backend_str = "qt"
    elif new_backend == "ipywidgets":
        from .backends.ipywidgets import IPYBackend

        # Prevent immediate display after calling plt.figure()
        import matplotlib
        matplotlib.pyplot.ioff()

        _backend = IPYBackend
        _backend_str = "ipywidgets"
    else:
        raise ValueError("Invalid backend") 
    

