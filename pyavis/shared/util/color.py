from typing import Tuple
from pyavis import _get_backend_str

color = Tuple[float,float,float] | Tuple[float,float,float,float] | Tuple[int,int,int] | Tuple[int,int,int,int] 

def _check_color(color):
    '''
    Check if value is of an accepted color format.

    Parameters
    ----------
    color
        Value to check
    '''
    if not isinstance(color, tuple):
        raise TypeError(f"'color' does not have the correct type. Type must be 'tuple'.")
    
    if len(color) != 3 and len(color) != 4:
        raise ValueError(f"'color' does not have the correct size. Size must be '3' or '4'.")
    
    for v in color:
        if not isinstance(v, float) and not isinstance(v, int):
            raise TypeError(f"'color' contains values of an incorrect type. Values must either be type 'int' or 'float'.")

    for v in color:
        if not type(v) is type(color[0]):
            raise TypeError("'color' contains mixed types. Use only one.")

def _convert_color(color):
    '''
    Convert the input color to a format used by the currently active backend.

    Parameters
    ----------
    color
        Value to convert
    '''
    _check_color(color)

    backend = _get_backend_str()
    if backend == "qt":
        return _qt_color(color)
    elif backend == "ipywidgets":
        return _mpl_color(color)
    else:
        raise TypeError(f"Unknown backend: {backend}")
    
def _qt_color(color):
    '''
    pyqtgraph uses color values between 0 - 255. Convert floats to integers if necessary.

    Parameters:
    -----------
    color:
        tuple of 'float' or 'int' values
    '''
    if isinstance(color[0], float):
        return tuple(map(lambda x: int(x * 255), list(color)))
    else:
        return color


def _mpl_color(color):
    '''
    matplotlib uses color values between 0.0 - 1.0. Convert integers to floats if necessary.

    Parameters:
    -----------
    color:
        tuple of 'float' or 'int' values
    '''
    if isinstance(color[0], int):
        return tuple(map(lambda x: x / 255, list(color)))
    else:
        return color

