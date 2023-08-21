from abc import abstractmethod
from typing import Literal
from pyavis.shared.util import Subject
from .graphic_element import GraphicElement

import numpy as np

class Signal(GraphicElement):
    def __init__(self):
        GraphicElement.__init__(self)
        self.dataChanged = Subject()
        self.sizeChanged = Subject()

        self.y_data = None
        self.y_data = None

    @abstractmethod
    def set_data(self, *args, **kwargs):
        '''
        Set the data that should be rendered.

        Parameters
        ----------
        y : np.ndarray
            y values, x values will be ``range(len(y))``
        x, y : np.ndarray, np.ndarray
            x, y values
        (y,) : Tuple[np.ndarray]
            y values given as tuple, x values will be ``range(len(y))``
        (x,y) : Tuple[np.ndarray, np.ndarray]
            x, y values given as tuple
        y=y : np.ndarray
            y values given as keyword argument, x values will be ``range(len(y))``
        x=x, y=y : np.ndarray, np.ndarray
             x, y values given as keyword argument
        '''

        x = None
        y = None

        if len(args) == 1:
            data = args[0]
            if isinstance(data, tuple):
                if len(data) == 1:
                    y = data[0]
                elif len(data) == 2:
                    x = data[0]
                    y = data[1]
                else:
                    raise ValueError("Too many entries in tuple")
            elif isinstance(data, np.ndarray):
                y = data
            else:
                raise TypeError("Not a valid type")
        elif len(args) == 2:
            x = args[0]
            y = args[1]
        
        if 'y' in kwargs:
            y = kwargs['y']
            if 'x' in kwargs:
                x = kwargs['x']

        self.y_data = y
        if x is None:
            self.x_data = np.arange(len(self.y_data))
        else:
            self.x_data = x
        
    
    @abstractmethod
    def set_vertical_size(self, size: float | Literal["auto"] = "auto"):
        '''
        Set the vertical size of the signal. "auto" uses the orignal values as size.

        Parameters:
        -----------
        size : float | str, default: "auto"
            New vetical size of the signal if float, else the orignal values as size
        '''
        pass
    
    @abstractmethod
    def set_style(self, style: dict | Literal["default"]):
        pass