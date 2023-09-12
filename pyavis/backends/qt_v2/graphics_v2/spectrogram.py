


import numpy as np
from typing import Tuple, Callable

from pya import Asig, Astft
from pyavis.backends.bases.graphic_bases_v2.spectrogram import Spectrogram

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.GraphicsScene.mouseEvents import *

class M_SpectrogramQt(type(Spectrogram), type(pg.ImageItem)): pass
class SpectrogramQt(Spectrogram, pg.ImageItem, metaclass=M_SpectrogramQt):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(
        self,
        data: Asig | Astft,
        position: Tuple[float, float] = (0.0, 0.0), 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
        with_bar = True,
        **kwargs
    ):
        if 'plt_item' not in kwargs:
            raise KeyError("PlotItem not provided. Cannot instantiate SpectrogramQt.")
        
        self.plt_item = kwargs['plt_item']

        Spectrogram.__init__(self, data, position, disp_func)
        pg.ImageItem.__init__(self, None)
        
        self.setImage(self.disp_func(self.orig_spectrogram.stft).T)
        self.setRect(*self.position, *(self.orig_spectrogram.times[-1], self.orig_spectrogram.freqs[-1]))

        self._c_bar = None
        self.toggle_color_bar(with_bar)

    def toggle_color_bar(self, show: bool):
        if show and self._c_bar is None:
            cbar = self.plt_item.addColorBar(self, colorMap='viridis', values=(0,1))
            self._c_bar = cbar
        elif not show and self._c_bar is not None:
            self.plt_item.getViewBox().removeItem(self._c_bar)
            self._c_bar = None

    def _update_plot(self):
        self.setRect(
            *self.position,
            self.orig_spectrogram.times[-1] * self.scale[0], 
            self.orig_spectrogram.freqs[-1] * self.scale[1]
        )

    def _abstract_set_active(self):
        if self.active:
            self.show()
        else:
            self.hide()
    
    def _abstract_set_position(self):
        self._update_plot()

    def _abstract_set_data(self):
        self.setImage(self.disp_func(self.orig_spectrogram.stft).T)
    
    def _abstract_set_scale(self):
        self._update_plot()

    def get_spectrogram_data(self):
        return self.image.T












    def mouseClickEvent(self, ev: MouseClickEvent):
        if self.clickable != True:
            return
        ev.accept()
        self.sigClicked.emit(self, ev)

        self.onClick.emit(self)

    def mouseDragEvent(self, ev: MouseDragEvent):
        if self.draggable != True:
            return
        ev.accept()
        self.sigDragged.emit(self, ev)

        if ev.isStart():
            self.onDraggingBegin.emit(self, ev.pos())
        elif ev.isFinish():
            self.onDraggingFinish.emit(self, ev.pos())
        else:
            self.onDragging.emit(self, ev.pos())
    
    def hoverEvent(self, ev: HoverEvent):
        self.sigHovered.emit(self, ev)