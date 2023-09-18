import numpy as np
from typing import Tuple, Callable
from pya import Asig, Astft

from pyavis.shared.util import Subject
from .graphic_element import GraphicElement



class Spectrogram(GraphicElement):
    def __init__(        
        self,
        data: Asig | Astft,
        position: Tuple[float, float] = (0.0, 0.0),
        scale: float = 1.0, 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
    ):
        GraphicElement.__init__(self, position)
        self.dataChanged = Subject()
        self.scaleChanged = Subject()

        self._internal_set_data(data)
        self.scale = scale
        self.disp_func = disp_func

    def set_data(self, data: Asig | Astft):
        '''
        Set the displayed Asig / Astft.

        Parameters
        ----------
        data: Asig | Astft
            Audio data to display
        '''
        self.set_data_silent(data)
        self.dataChanged.emit(self)

    def set_data_silent(self, data: Asig | Astft):
        '''
        Set the displayed Asig / Astft
        Does not trigger observers.

        Parameters
        ----------
        data: Asig | Astft
            Audio data to display
        '''
        self._internal_set_data(data)
        self._abstract_set_data()

    def _internal_set_data(self, data: Asig | Astft):
        '''
        Set the displayed Asig / Astft.
        For internal use only.

        Parameters
        ----------
        data: Asig | Astft
            Audio data to display
        '''
        if type(data) == Asig:
            self.orig_signal = data
            self.orig_spectrogram = data.to_stft()
        elif type(data) == Astft:
            self.orig_signal = None
            self.orig_spectrogram = data
        else:
            raise TypeError("Unknown data, should be either Asig or Astft")

    def _abstract_set_data(self):
        pass

    def toggle_color_bar(self, show: bool):
        pass

    def get_spectrogram_data(self):
        pass
        

    def set_scale(self, scale: Tuple[float, float]):
        '''
        Set the displayed scale of the spectrogram. Default size
        is corresponds to signal length in seconds and highest frequency of the STFT.

        Parameter
        ---------
        scale: (float, float)
            x and y scale
        '''
        old_scale = self.scale

        self.set_scale_silent(scale)
        self.scaleChanged.emit(self, self.scale, old_scale)

    def set_scale_silent(self, scale: Tuple[float, float]):
        '''
        Set the displayed scale of the spectrogram. Default size
        is corresponds to signal length in seconds and highest frequency of the STFT.
        Does not trigger observers.

        Parameter
        ---------
        scale: (float, float)
            x and y scale
        '''

        self._internal_set_scale(scale)
        self._abstract_set_scale()

    def _internal_set_scale(self, scale: Tuple[float, float]):
        '''
        Set the displayed scale of the spectrogram. Default size
        is corresponds to signal length in seconds and highest frequency of the STFT.
        For internal use only.

        Parameter
        ---------
        scale: (float, float)
            x and y scale
        '''
        self.scale = scale

    def _abstract_set_scale(self):
        pass
    
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