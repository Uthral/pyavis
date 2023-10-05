import numpy as np
from typing import Any, Literal, Tuple, Callable
from pya import Asig, Aspec

from pyavis.shared.util import Subject
from .graphic_element import GraphicElement

class Spectrum(GraphicElement):
    """
    Base class representing a renderable spectrum.
    """
    def __init__(        
        self,
        data: Asig | Aspec,
        position: Tuple[float, float] = (0.0, 0.0),
        scale: float = 1.0, 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
    ):
        """
        Construct a new spectrum render.

        Parameters
        ----------
        data : Asig | Aspec
            Signal / FFT to render
        position : Tuple[float, float], optional
            Position of the spectrum, by default (0.0, 0.0)
        scale : float, optional
            Scale of the spectrum, by default 1.0
        disp_func : Callable[[np.ndarray], np.ndarray], optional
            Function applied to the spectrum data, by default np.abs
        """
        GraphicElement.__init__(self, position)
        self.dataChanged = Subject()
        self.scaleChanged = Subject()

        self._set_data(data)
        self.scale = scale
        self.disp_func = disp_func

    def set_data(self, data: Asig | Aspec, trigger = True):
        """
        Set the displayed Asig / Aspec.

        Parameters
        ----------
        data : Asig | Aspec
            Audio data to display
        trigger : bool, optional
            Trigger obeserver, by default True
        """
        self._set_data(data)
        self._abstract_set_data()

        if trigger:
            self.dataChanged.emit(self)

    def _set_data(self, data: Asig | Aspec):
        if type(data) == Asig:
            self.orig_signal = data
            self.orig_spec = data.to_spec()
        elif type(data) == Aspec:
            self.orig_signal = None
            self.orig_spec = data
        else:
            raise TypeError("Unknown data, should be either Asig or Aspec")
        
    def set_scale(self, scale: float, trigger = True):
        """
        Set the displayed scale of the spectrum.

        Parameter
        ---------
        scale: float
            

        Parameters
        ----------
        scale : float
            y scale of the spectrum
        """
        old_scale = self.scale
        if old_scale[0] == scale[0] and old_scale[1] == scale[1]:
            return
        
        self.scale = scale
        self._abstract_set_scale()
        
        if trigger:
            self.scaleChanged.emit(self, self.scale, old_scale)

    def set_style(self, line_color: Any | Literal["default"]):
        """
        Set the color of the spectrum.

        Parameters
        ----------
        line_color : color | "default"
            Either "default" or color
        """
        if line_color == "default":
            from pyavis.config import get_style_config_value
            line_color = get_style_config_value("line_color")
        else:
            from pyavis.shared.util import color
            color._check_color(line_color)
        
        self._abstract_set_style(line_color)

    def _abstract_set_scale(self):
        pass

    def _abstract_set_data(self):
        pass

    def _abstract_set_style(self, line_color: Any):
        pass
