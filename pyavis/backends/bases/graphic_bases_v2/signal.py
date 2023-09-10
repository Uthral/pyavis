from abc import abstractmethod
from typing import Any, Literal, Tuple
import numpy as np

from .graphic_element import GraphicElement
from pyavis.shared.util import Subject

class Signal(GraphicElement):
    def __init__(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            vertical_size: float | Literal["auto"] = "auto",
            *args,
            **kwargs,

        ):
        GraphicElement.__init__(self, position)
        self.dataChanged = Subject()
        self.sizeChanged = Subject()

        self.x_data = None
        self.y_data = None
        self.y_data_sized = None
        self.vert_size = None

        self._internal_set_data(*args, **kwargs)
        self._internal_set_vertical_size(vertical_size)
        

    def set_data(self, *args, **kwargs):
        self.set_data_silent(*args, **kwargs)
        self.dataChanged.emit(self)

    def set_data_silent(self, *args, **kwargs):
        '''
        Set the data that should be rendered.
        Does not trigger observers.

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
        self._internal_set_data(*args, **kwargs)
        if self.vert_size != "auto":
            self._internal_set_vertical_size(self.vert_size)

        self._abstract_set_data()


    def _internal_set_data(self, *args, **kwargs):
        '''
        For interal use only.
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
    def _abstract_set_data(self):
        pass


    def set_vertical_size(self, vert_size: float | Literal["auto"] = "auto"):
        '''
        Set the vertical size of the signal. "auto" uses the orignal values as size.

        Parameters:
        -----------
        vert_size : float | str, default: "auto"
            New vetical size of the signal if float, else the orignal values as size
        '''
        if vert_size == vert_size:
            return

        self.set_vertical_size_silent(vert_size)
        self.sizeChanged.emit(self)
    
    def set_vertical_size_silent(self, vert_size: float | Literal["auto"] = "auto"):
        '''
        Set the vertical size of the signal. "auto" uses the orignal values as size.
        Does not trigger observers.

        Parameters:
        -----------
        vert_size : float | str, default: "auto"
            New vetical size of the signal if float, else the orignal values as size
        '''
        self._internal_set_vertical_size(vert_size)
        self._abstract_set_vertical_size()

    
    def _internal_set_vertical_size(self, vert_size: float | Literal["auto"] = "auto"):
        '''
        For internal usage only.
        Set the size of the signal.

        vert_size : float | str, default: "auto"
            New vetical size of the signal if float, else the orignal values as size
        '''
        self.vert_size = vert_size

        if self.x_data is None or self.y_data is None:
            return

        if self.vert_size == "auto":
            self.y_data_sized = self.y_data.view()
        else:
            self.y_data_sized = (self.y_data / np.max(self.y_data)) * (self.vert_size / 2)

    @abstractmethod
    def _abstract_set_vertical_size(self):
        pass












    
    def set_style(self, line_color: Any | Literal["default"] = "default"):
        '''
        Set the color of the signal.

        Parameters
        ----------
        line_color : (int,int,int) | (int,int,int,int) | str, default: "default"
            Either "default" or values accepted by `pg.mkColor`
        '''
        if line_color == "default":
            from pyavis.config import get_style_config_value
            line_color = get_style_config_value("line_color")
        else:
            from pyavis.shared.util import color
            color._check_color(line_color)
        
        self._abstract_set_style(line_color)

    def _abstract_set_style(self, line_color: Any):
        pass