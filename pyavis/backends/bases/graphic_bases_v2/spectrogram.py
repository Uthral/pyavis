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
        Set the displayed data of the spectrogram.

        Parameters
        ----------
        data: Asig | Astft
            Audio data to display
        '''
        self.set_data_silent(data)
        self.dataChanged.emit(self)

    def toggle_color_bar(self, show: bool):
        pass
        
    def set_data_silent(self, data: Asig | Astft):
        '''
        Set the displayed data of the spectrogram.
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
        Set the displayed data of the spectrogram.
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

    def draw(self, draw_info):
        '''
        Draw into the spectrogram using the provided drawing information.
        '''
        pass

def spec_to_stft(spectrogram: Spectrogram):
    pass

def spec_to_asig(spectrogram: Spectrogram):
    pass