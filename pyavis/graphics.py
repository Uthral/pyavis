from . import _get_backend
from .backends import Backend
from .backends.bases.graphic_bases import Layout as GFXLayout, Track as GFXTrack 

def _is_missing_implementation(backend: Backend, gfx: str):
    if gfx not in backend.get_gfx_registry():
        class_name = repr(backend)[7:-1]
        raise RuntimeError(f'{class_name} does not implement {gfx}')
    
def _get_implementation(gfx: str):
    backend = _get_backend()
    _is_missing_implementation(backend, gfx)
    return backend.get_gfx_registry()[gfx]

def Layout(*args, **kwargs) -> GFXLayout:
    return _get_implementation('Layout')(*args, **kwargs)

def Track(*args, **kwargs) -> GFXTrack:
    return _get_implementation('Track')(*args, **kwargs)