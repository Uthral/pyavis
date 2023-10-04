from abc import abstractmethod
from typing import Any, Literal, Tuple
import numpy as np

from .graphic_element import GraphicElement
from pyavis.shared.util import Subject

class Signal(GraphicElement):
    """
    Base class representing a renderable signal.
    """
    def __init__(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            scale: float = 1.0,
            *args,
            **kwargs,

        ):
        """
        Construct a new signal render.

        Parameters
        ----------
        position : Tuple[float, float], optional
            Postition of the signal, by default (0.0, 0.0)
        scale : float, optional
            Scale of the signal, by default 1.0
        *args, **kwargs
            Arguments are passed to :func:Signal.set_data()

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
        """
        GraphicElement.__init__(self, position)
        self.dataChanged = Subject()
        self.scaleChanged = Subject()

        self.x_data = None
        self.y_data = None
        self.y_data_scaled = None
        
        self.scale = scale

        self._update_data(*args, **kwargs)
        self._update_scale()

    def set_data(self, *args, **kwargs):
        """
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
        """
        self._update_data(*args, **kwargs)  
        self._update_scale()
        self._abstract_set_data()

        self.dataChanged.emit(self)

    def set_scale(self, scale: float = 1.0, trigger = True):
        """
        Set the scale of the y values.

        Parameters
        ----------
        scale : float, optional
            Scale of the y values, by default 1.0
        trigger : bool, optional
            Trigger observer, by default True
        """
        
        old_scale = self.scale
        if old_scale == scale:
            return
        
        self.scale = scale
        if self.x_data is None or self.y_data is None:
            return
        
        self._update_scale()
        self._abstract_set_scale()

        self.scaleChanged.emit(self, self.scale, old_scale)

    def _update_data(self, *args, **kwargs):
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
            if len(x) != len(y):
                raise ValueError("Length missmatch")
            self.x_data = x 

    def _update_scale(self):
        if self.scale == 1.0:
            self.y_data_scaled = self.y_data.view()
        else:
            self.y_data_scaled = self.y_data * self.scale
    
    def set_style(self, line_color: Any | Literal["default"] = "default"):
        """
        Set the color of the signal.

        Parameters
        ----------
        line_color : color.color | str, default: "default"
            Either "default" or values of the format 'color.color'
        """
        if line_color == "default":
            from pyavis.config import get_style_config_value
            line_color = get_style_config_value("line_color")
        else:
            from pyavis.shared.util import color
            color._check_color(line_color)
        
        self._abstract_set_style(line_color)

    def _abstract_set_data(self):
        pass

    def _abstract_set_scale(self):
        pass

    def _abstract_set_style(self, line_color: Any):
        pass