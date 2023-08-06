


from pyavis.base_classes import AbstractSpectrogramVisualizer

import pyqtgraph as pg
import numpy as np
from pya import Asig, Astft, ampdb

#TODO: At basic drawing (e.g. set area to 0)
#TODO: At basic styling & display (Hz, dB, maybe color)
#TODO: Add selection & save

class SpectogramQt(AbstractSpectrogramVisualizer):
    def __init__(self, x: Asig | Astft, *args, **kwargs):
        self.widget = pg.GraphicsLayoutWidget(*args, **kwargs)
        self.plot = self.widget.addPlot()
        self.img = pg.ImageItem()

        self.plot.addItem(self.img)
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img)
        self.widget.addItem(self.hist)

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
        
        self.hist.setLevels(np.min(np.abs(stft)), np.max(np.abs(stft)))
        self.hist.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(1.0, (245, 175, 25, 255)),
                   (0.5, (195, 20, 50, 255)),
                   (0.0, (36, 11, 54, 255))]})



        self.img.setImage(ampdb(np.abs(stft.T)))
        self.img.setRect(0,0,times[-1],freqs[-1])
        self.plot.setLimits(xMin=0, xMax=times[-1], yMin=0, yMax=freqs[-1])


    def get_native_widget(self: bool):
        return self.widget