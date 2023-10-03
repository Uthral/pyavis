from typing import Tuple
from pyavis import _get_backend_str

import numpy as np


color = Tuple[float,float,float] | Tuple[float,float,float,float] | Tuple[int,int,int] | Tuple[int,int,int,int] 

def _check_color(color: color):
    """
    Validate if value is of an accepted color format.

    Parameters
    ----------
    color : color
        Value to validate

    Raises
    ------
    TypeError
        Raised if color is not a tuple, color does not have length 3 or 4, values are not int or float or if types are mixed
    """
    if not isinstance(color, tuple):
        raise TypeError(f"'color' does not have the correct type. Type must be 'tuple'.")
    
    if len(color) != 3 and len(color) != 4:
        raise TypeError(f"'color' does not have the correct size. Size must be '3' or '4'.")
    
    for v in color:
        if not isinstance(v, float) and not isinstance(v, int):
            raise TypeError(f"'color' contains values of an incorrect type. Values must either be type 'int' or 'float'.")

    for v in color:
        if not type(v) is type(color[0]):
            raise TypeError("'color' contains mixed types. Use only one.")

def _convert_color(color: color) -> color:
    """
    Convert input color to a format used by the currently active backend.

    Parameters
    ----------
    color : color
        Color to convert

    Returns
    -------
    color
        Color in the correct format for the current backend

    Raises
    ------
    RuntimeError
        Raised if unknown backend is used
    """
    _check_color(color)

    backend = _get_backend_str()
    if backend == "qt":
        return _qt_color(color)
    elif backend == "ipywidgets":
        return _mpl_color(color)
    else:
        raise RuntimeError(f"Unknown backend: {backend}")
    
def _qt_color(color: color) -> color:
    """
    pyqtgraph uses color values between 0 - 255. Convert floats to integers if necessary.

    Parameters
    ----------
    color : color
        tuple of 'float' or 'int' values

    Returns
    -------
    color
        tuple of integers in the range of 0 - 255
    """
    if isinstance(color[0], float):
        return tuple(map(lambda x: np.clip(int(x * 255), 0, 255), list(color)))
    else:
        return tuple(np.clip(color, 0, 255))


def _mpl_color(color: color) -> color:
    """
    matplotlib uses color values between 0.0 - 1.0. Convert integers to floats if necessary.

    Parameters
    ----------
    color : color
        tuple of 'float' or 'int' values

    Returns
    -------
    color
        tuple of floats in the range of 0.0 - 1.0
    """
    if isinstance(color[0], int):
        return tuple(map(lambda x: np.clip(x / 255, 0.0, 1.0), list(color)))
    else:
        return tuple(np.clip(color, 0.0, 1.0))

