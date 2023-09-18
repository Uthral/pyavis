from . import _get_backend
from .backends import Backend
from .backends.bases.graphic_bases import Rectangle, Signal, Selection, Axis, Track, MultiTrack, Spectrogram, Line


def _is_missing_implementation(backend: Backend, gfx: str):
    if gfx not in backend.get_gfx_registry():
        class_name = repr(backend)[7:-1]
        raise RuntimeError(f'{class_name} does not implement {gfx}')
    
def _get_implementation(gfx: str):
    backend = _get_backend()
    _is_missing_implementation(backend, gfx)
    return backend.get_gfx_registry()[gfx]

def createRectangle(*args, **kwargs) -> Rectangle:
    return _get_implementation('Rectangle')(*args, **kwargs)

def createSignal(*args, **kwargs) -> Signal:
    return _get_implementation('Signal')(*args, **kwargs)

def createSelection(*args, **kwargs) -> Selection:
    return _get_implementation('Selection')(*args, **kwargs)

def createAxis(*args, **kwargs) -> Axis:
    return _get_implementation('Axis')(*args, **kwargs)

def createTrack(*args, **kwargs) -> Track:
    return _get_implementation('Track')(*args, **kwargs)

def createMultiTrack(*args, **kwargs) -> MultiTrack:
    return _get_implementation('MultiTrack')(*args, **kwargs)

def createSpectrogram(*args, **kwargs) -> Spectrogram:
    return _get_implementation('Spectrogram')(*args, **kwargs)

def createLine(*args, **kwargs) -> Line:
    return _get_implementation('Line')(*args, **kwargs)



from .backends.bases.graphic_bases_v2 import Layout, Track 

def Layout_v2(*args, **kwargs) -> Layout:
    return _get_implementation('Layout_v2')(*args, **kwargs)

def Track_v2(*args, **kwargs) -> Track:
    return _get_implementation('Track_v2')(*args, **kwargs)