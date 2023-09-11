import numpy as np
from typing import Tuple, Callable
from pya import Asig, Astft
from .graphic_element import GraphicElement

class Spectrogram(GraphicElement):
    def __init__(        self,
        data: Asig | Astft,
        position: Tuple[float, float] = (0.0, 0.0), 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
    ):
        GraphicElement.__init__(self, position)

        if type(data) == Asig:
            self.orig_signal = data
            self.orig_spectrogram = data.to_stft()
        elif type(data) == Astft:
            self.orig_signal = None
            self.orig_spectrogram = data
        else:
            raise TypeError("Unknown data type x, x should be either Asig or Astft")
        self.disp_func = disp_func