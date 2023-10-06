import numpy as np
from typing import Tuple, Callable
from pya import Asig, Astft

from pyavis.shared.util import Subject
from .graphic_element import GraphicElement

class Spectrogram(GraphicElement):
    """
    Base class representing a renderable spectrogram.
    """
    def __init__(        
        self,
        data: Asig | Astft,
        position: Tuple[float, float] = (0.0, 0.0),
        scale: Tuple[float, float] = (1.0, 1.0), 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
        **kwargs
    ):
        """
        Construct a new spectrogram render.

        Parameters
        ----------
        data : Asig | Astft
            Signal / STFT to render
        position : Tuple[float, float], optional
            Position of the spectrogram, by default (0.0, 0.0)
        scale : float, optional
            Scale of the spectrogram, by default 1.0
        disp_func : Callable[[np.ndarray], np.ndarray], optional
            Function applied to the spectrogram data, by default np.abs
        """
        GraphicElement.__init__(self, position)
        self.dataChanged = Subject()
        self.scaleChanged = Subject()

        self._set_data(data, **kwargs)
        self.scale = scale
        self.disp_func = disp_func

    def toggle_color_bar(self, show: bool):
        pass

    def set_data(self, data: Asig | Astft, trigger = True):
        """
        Set the displayed Asig / Astft.

        Parameters
        ----------
        data : Asig | Astft
            Audio data to display
        trigger : bool, optional
            Trigger obeserver, by default True
        """
        self._set_data(data)
        self._abstract_set_data()

        if trigger:
            self.dataChanged.emit(self)

    def _set_data(self, data: Asig | Astft, **kwargs):
        if type(data) == Asig:
            self.orig_signal = data
            self.orig_spectrogram = data.to_stft(**kwargs)
        elif type(data) == Astft:
            self.orig_signal = None
            self.orig_spectrogram = data
        else:
            raise TypeError("Unknown data, should be either Asig or Astft")

    def set_scale(self, scale: Tuple[float, float], trigger = True):
        """
        Set the displayed scale of the spectrogram. Default size
        is corresponds to signal length in seconds and highest frequency of the STFT.

        Parameter
        ---------
        scale: (float, float)
            

        Parameters
        ----------
        scale : Tuple[float, float]
            x and y scale of the spectrogram
        """
        old_scale = self.scale
        if old_scale[0] == scale[0] and old_scale[1] == scale[1]:
            return
        
        self.scale = scale
        self._abstract_set_scale()
        
        if trigger:
            self.scaleChanged.emit(self, self.scale, old_scale)
        
    
    def get_spectrogram_data(self):
        '''
        Get the data of the displayed spectrogram.
        '''
        pass

    def draw(self, freq: float, time: float):
        '''
        Draw into the spectrogram using at the provided frequency and time.
        Drawing is limited by resolution of spectrogram.

        Parameters
        ----------
        freq: float
            Frequency to draw at
        time: float
            Time to draw at
        '''
        pass

    def set_brush(self, brush_data=None, brush_mask=None, brush_center=(0,0), draw_mode="set"):
        """ 
        Set the brush shape, values, center and mode.

        Parameters
        ----------
        brush_data : np.ndarray, default: None
            Values that should be used for drawing
        brush_mask : np.ndarray, optional, default: None
            Mask with values between 0-1. Effect: image * (1-mask) + data * mask
        brush_center : tuple, default: (0, 0)
            Center of the brush
        draw_mode : str, optional, default: "set"
            Either "add" or "set". If "set", then mask will be ignored.
        """
    
    def clear_brush(self):
        '''
        Clear the brush.
        '''


    def _abstract_set_scale(self):
        pass

    def _abstract_set_data(self):
        pass