from . import _get_backend
from .backends import Backend
from .backends.bases.graphic_bases import Layout 

def _is_missing_implementation(backend: Backend, gfx: str):
    if gfx not in backend.get_gfx_registry():
        class_name = repr(backend)[7:-1]
        raise RuntimeError(f'{class_name} does not implement {gfx}')
    
def _get_implementation(gfx: str):
    backend = _get_backend()
    _is_missing_implementation(backend, gfx)
    return backend.get_gfx_registry()[gfx]

def Layout(rows: int = 1, columns: int = 1) -> Layout:
    """
    Construct a new layout.

    Parameters
    ----------
    rows : int, optional
        Row count, by default 1
    columns : int, optional
        Column count, by default 1

    Returns
    -------
    Layout
        Newly constructed layout
    """
    return _get_implementation('Layout')(rows, columns)
