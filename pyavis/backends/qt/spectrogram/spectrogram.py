
from copy import deepcopy

from pyavis.base_classes import AbstractSpectrogramVisualizer

import pyqtgraph as pg
import numpy as np

from typing import Callable
from pyqtgraph.Qt import QtCore
from pya import Asig, Astft

#TODO: Allow better control over brush size / shape / ...
#TODO: Add basic styling & display (Hz, dB, maybe color)

class SpectogramQt(AbstractSpectrogramVisualizer):
    def __init__(self, x: Asig | Astft, disp_func: Callable[[np.ndarray], np.ndarray] = np.abs, *args, **kwargs):
        self.widget = pg.GraphicsLayoutWidget(*args, **kwargs)
        self.hist = pg.HistogramLUTItem()
        self.img = pg.ImageItem()

        self.plot = self.widget.addPlot()
        self.plot.addItem(self.img)

        self.hist.setImageItem(self.img)
        self.widget.addItem(self.hist)

        self.disp_func = disp_func
        if type(x) == Asig:
            self.orig_signal = x
            self.orig_spectrogram = x.to_stft()
        elif type(x) == Astft:
            self.orig_signal = None
            self.orig_spectrogram = x
        else:
            raise TypeError("Unknown data type x, x should be either Asig or Astft")
        
        freqs = self.orig_spectrogram.freqs
        times = self.orig_spectrogram.times
        stft = self.orig_spectrogram.stft

        # TODO: Display function can drastically change value of image
        #       E.g. magnitude values in decible -> negative numbers 
        #       -> can this be handled reasonably
        disp = self.disp_func(stft)
        
        self.hist.setLevels(np.min(disp), np.max(disp))
        self.hist.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(1.0, (245, 175, 25, 255)),
                   (0.5, (195, 20, 50, 255)),
                   (0.0, (36, 11, 54, 255))]})

        self.img.setImage(disp.T)        
        self.img.setRect(0,0,times[-1],freqs[-1])
        self.plot.setLimits(xMin=0, xMax=times[-1], yMin=0, yMax=freqs[-1])


    def get_native_widget(self: bool):
        return self.widget
    
    def reset(self):
        self.img.setImage(np.abs(self.orig_spectrogram.stft.T))

    def return_as_asig(self) -> Asig:
        # Image is transposed spectrum -> Transpose again
        # Image is absolute value of STFT (magnitude)
        # Potential solutions:
        #   - Normalize original STFT and scale with image magnitudes
        magnitude = self.img.image.T
        norm_stft = self.orig_spectrogram.stft / np.abs(self.orig_spectrogram.stft)
        stft = deepcopy(self.orig_spectrogram)

        stft.stft = magnitude * norm_stft
        stft.label = stft.label + '_edited'
        return stft.to_sig()

    def return_as_astft(self) -> Astft:
        # Image is transposed spectrum -> Transpose again
        # Image is absolute value of STFT (magnitude)
        # Potential solutions:
        #   - Normalize original STFT and scale with image magnitudes
        magnitude = self.img.image.T
        norm_stft = self.orig_spectrogram.stft / np.abs(self.orig_spectrogram.stft)
        stft = deepcopy(self.orig_spectrogram)

        stft.stft = magnitude * norm_stft
        stft.label = stft.label + '_edited'
        return stft

    def draw(self, freq: float, time: float):
        adj_freq = freq / ((self.orig_spectrogram.sr / 2) / len(self.orig_spectrogram.freqs))
        adj_time = (time / ((self.orig_spectrogram.samples / self.orig_spectrogram.sr))) * len(self.orig_spectrogram.times)
        pos = QtCore.QPointF(adj_time, adj_freq)

        self.img.setDrawKernel(kernel=np.ones((50,2)), mask=np.ones((50,2)), center=(5,1), mode='set')
        self.img.drawAt(pos)
        self.img.setDrawKernel()

    def set_draw_shape(self, data):
        # self.brush_data = ...
        # self.brush_mask = ...
        # self.draw_mode = "add" or "set" or func
        pass

    def draw_mode(self, active: bool = False):
        # if active:
        #   self.img.setDrawKernel(...)
        # else:
        #   self.img.setDrawKernel()
        pass
        
