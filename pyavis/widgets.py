from typing import Any, List, Literal
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

from .backends.bases.widget_bases import (
    BaseButton,
    BaseToggleButton,
    BaseFloatSlider, 
    BaseHBox, 
    BaseIntSlider, 
    BaseDropDown, 
    BaseScrollArea, 
    BaseVBox,
    BaseGraphicDisp
)

def Button(label: str) -> BaseButton:
    return _get_implementation('Button')(label)

def ToggleButton(label: str, icon: Any = None, default_toggle_state: bool = False) -> BaseToggleButton:
    return _get_implementation('ToggleButton')(label, icon, default_toggle_state)

def VBox() -> BaseVBox:
    return _get_implementation('VBox')()

def HBox() -> BaseHBox:
    return _get_implementation('HBox')()

def IntSlider(
    description: str, 
    orientation: Literal["vertical", "horizontal"], 
    default: int = 50, 
    min: int = 1,
    max: int = 100, 
    step: int = 1
) -> BaseIntSlider:
    return _get_implementation('IntSlider')(description, orientation, default, min, max, step)

def FloatSlider(
        description: str,
        orientation: Literal["vertical", "horizontal"], 
        default: float = 5.0, 
        min: float = 1.0, 
        max: float = 10.0, 
        step: float = 0.1
) -> BaseFloatSlider:
    return _get_implementation('FloatSlider')(description, orientation, default, min, max, step)

def DropDown(description: str, options: List[Any], default: Any = None) -> BaseDropDown:
    return _get_implementation('DropDown')(description, options, default)

def ScrollArea(height: int = 100) -> BaseScrollArea:
    return _get_implementation('ScrollArea')(height)

def GraphicDisp() -> BaseGraphicDisp:
    return _get_implementation('GraphicDisp')()