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
    BaseGraphicDisp,
    BaseToolbar
)

def Button(label: str) -> BaseButton:
    """
    Construct a new button.

    Parameters
    ----------
    label : str
        Label of the button

    Returns
    -------
    BaseButton
        Newly created button widget
    """
    return _get_implementation('Button')(label)

def ToggleButton(label: str, icon: Any = None, default_toggle_state: bool = False) -> BaseToggleButton:
    """
    Construct a new toggable button.

    Parameters
    ----------
    label : str
        Label of the button
    icon : Any, optional
        Icon of the button, by default None. Has to be specified
    default_toggle_state : bool, optional
        Default state of the button, by default False

    Returns
    -------
    BaseToggleButton
        Newly created button widget
    """
    return _get_implementation('ToggleButton')(label, icon, default_toggle_state)

def Toolbar(labels: List[str], values: List[str]) -> BaseToolbar:
    """
    Construct a new toolbar.

    Parameters
    ----------
    labels : List[str]
        Labels of the toolbar buttons
    values : List[str]
        Values of the toolbar buttons

    Raises
    ------
    RuntimeError
        Raises if labels and values have different lengths
    
    Returns
    -------
    BaseToolbar
        Widget for vertical layouting
    """
    return _get_implementation('Toolbar')(labels, values)

def VBox() -> BaseVBox:
    """
    Construct a vertical layouting widget.

    Returns
    -------
    BaseVBox
        Widget for vertical layouting
    """
    return _get_implementation('VBox')()

def HBox() -> BaseHBox:
    """
    Create horizontal layouting widget.

    Returns
    -------
    BaseHBox
        Widget for horizontal layouting
    """
    return _get_implementation('HBox')()

def IntSlider(
    description: str, 
    orientation: Literal["vertical", "horizontal"], 
    default: int = 50, 
    min: int = 1,
    max: int = 100, 
    step: int = 1
) -> BaseIntSlider:
    """
    Construct a new integer slider widget.

    Parameters
    ----------
    description : str
        Description of the slider
    orientation : Literal[&quot;vertical&quot;, &quot;horizontal&quot;]
        Orientation of the slider
    default : int, optional
        Default value of the slider, by default 50
    min : int, optional
        Minimum value of the slider, by default 1
    max : int, optional
        Maximum value of the slider, by default 100
    step : int, optional
        Step size in which the slider can be incremented, by default 1

    Returns
    -------
    BaseIntSlider
        Newly created integer slider widget
    """
    return _get_implementation('IntSlider')(description, orientation, default, min, max, step)

def FloatSlider(
        description: str,
        orientation: Literal["vertical", "horizontal"], 
        default: float = 5.0, 
        min: float = 1.0, 
        max: float = 10.0, 
        step: float = 0.1
) -> BaseFloatSlider:
    """
    Construct a new float slider widget.

    Parameters
    ----------
    description : str
        Orientation of the slider
    orientation : Literal[&quot;vertical&quot;, &quot;horizontal&quot;]
        Orientation of the slider
    default : float, optional
        Default value of the slider, by default 5.0
    min : float, optional
        Minimum value of the slider, by default 1.0
    max : float, optional
        Maximum value of the slider, by default 10.0
    step : float, optional
        Step size in which the slider can be incremented, by default 0.1

    Returns
    -------
    BaseFloatSlider
        Newly created float slider widget
    """
    return _get_implementation('FloatSlider')(description, orientation, default, min, max, step)

def DropDown(description: str, options: List[Any], default: Any = None) -> BaseDropDown:
    """
    Construct a new drop down widget.

    Parameters
    ----------
    description : str
        Description of the drop down.
    options : List[Any]
        Selectable options of the drop down.
    default : Any, optional
        Default value of the drop down, by default None

    Returns
    -------
    BaseDropDown
        Newly created drop down widget
    """
    return _get_implementation('DropDown')(description, options, default)

def ScrollArea(height: int = 100, width: int = 100) -> BaseScrollArea:
    """
    Construct a new scrollable widget container.

    Parameters
    ----------
    height : int, optional
        Height of the scrollable area, by default 100
    width : int, optional
        Width of the scrollable area, by default 100

    Returns
    -------
    BaseScrollArea
        Newly created scrollable widget container
    """
    return _get_implementation('ScrollArea')(height=height, width=width)

def GraphicDisp() -> BaseGraphicDisp:
    """
    Construct a new graphics display.

    Returns
    -------
    BaseGraphicDisp
        Widget for displaying graphics
    """
    return _get_implementation('GraphicDisp')()