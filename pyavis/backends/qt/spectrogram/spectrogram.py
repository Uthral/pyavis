
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
        '''
        Reset the image to the origninal :class:`Astft <pya.Astft>`
        '''
        self.img.setImage(np.abs(self.orig_spectrogram.stft.T))

    def return_as_asig(self, **kwargs) -> Asig:
        '''
        Return the displayed STFT as an :class:`Asig <pya.Asig>`.

        Parameters
        ----------
        **kwargs :
            Keyword arguments for :func:`Astft.to_sig()`
        '''

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
        '''
        Return the displayed STFT as an :class:`Astft <pya.Astft>`
        '''

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
        '''
        Draw at the time and position with the set brush.
        Does nothing if no brush data is set.

        Parameters
        ----------
        freq: float
            Frequencey to draw at
        time: float
            Time to draw at
        '''
        adj_freq = freq / ((self.orig_spectrogram.sr / 2) / len(self.orig_spectrogram.freqs))
        adj_time = (time / ((self.orig_spectrogram.samples / self.orig_spectrogram.sr))) * len(self.orig_spectrogram.times)
        pos = QtCore.QPointF(adj_time, adj_freq)

        # Enable draw mode for the operation, disable afterwards.
        if self.brush_data is not None:
            self.draw_mode(True)
            self.img.drawAt(pos)
            self.draw_mode(False)

    def set_brush_data(self, brush_data=None, brush_mask=None, brush_center=(0,0), draw_mode="add"):
        """ 
        Set the brush shape, values, center and mode.
        See :function:`drawAt` from :class:`ImageItem <pyqtgraph.ImageItem>` for more details.

        Parameters
        ----------
        brush_data : np.ndarray, default: None
            Values that should be used for drawing
        brush_mask : np.ndarray, optional, default: None
            Mask with values between 0-1. Effect: image * (1-mask) + data * mask
        brush_center : tuple, default: (0, 0)
            Center of the brush
        draw_mode : str, optional, default: "add"
            Either "add" or "set". If "set", then mask will be ignored.
        """
        self.brush_data = brush_data
        self.brush_mask = brush_mask
        self.brush_center = brush_center
        self.brush_mode = draw_mode
        
    def draw_mode(self, active: bool = False):
        """ 
        Enable or disable draw mode.
        """
        if active:
           self.img.setDrawKernel(self.brush_data, self.brush_mask, self.brush_center, self.brush_mode)
        else:
           self.img.setDrawKernel()