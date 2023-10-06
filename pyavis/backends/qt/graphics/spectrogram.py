


import numpy as np
from typing import Tuple, Callable

from pya import Asig, Astft
from pyavis.backends.bases.graphic_bases.spectrogram import Spectrogram

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.GraphicsScene.mouseEvents import *

class M_SpectrogramQt(type(Spectrogram), type(pg.ImageItem)): pass
class SpectrogramQt(Spectrogram, pg.ImageItem, metaclass=M_SpectrogramQt):
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
        
        self.plt_item = kwargs.pop('plt_item')

        Spectrogram.__init__(self, data, position, 1, disp_func, **kwargs)
        pg.ImageItem.__init__(self, None)
        
        self.setImage(self.disp_func(self.orig_spectrogram.stft).T)
        self.setRect(*self.position, *(self.orig_spectrogram.times[-1], self.orig_spectrogram.freqs[-1]))

        self._c_bar = None
        self.toggle_color_bar(with_bar)

    def toggle_color_bar(self, show: bool):
        if show and self._c_bar is None:
            cbar = self.plt_item.addColorBar(self, colorMap='viridis', values=(0,1))
            
            # Colorbar does not adjust automatically, set on creation
            min_val, max_val = np.min(self.image), np.max(self.image)
            cbar.setLevels((min_val, max_val))

            self._c_bar = cbar
        elif not show and self._c_bar is not None:
            self.plt_item.getViewBox().removeItem(self._c_bar)
            self._c_bar = None





    def draw(self, freq: float, time: float):
        adj_freq = freq / ((self.orig_spectrogram.sr / 2) / len(self.orig_spectrogram.freqs))
        adj_time = (time / ((self.orig_spectrogram.samples / self.orig_spectrogram.sr))) * len(self.orig_spectrogram.times)
        pos = QtCore.QPointF(adj_time, adj_freq)

        if hasattr(self, '_brush_set') and self._brush_set:
            self.setDrawKernel(self._brush_data, self._brush_mask, self._brush_center, self._brush_mode)
            self.drawAt(pos)
            self.setDrawKernel()
        else:
            raise RuntimeError("No brush was set. Set a brush before drawing")

    def set_brush(self, brush_data=None, brush_mask=None, brush_center=(0,0), draw_mode="set"):
        """ 
        See :function:`drawAt` from :class:`ImageItem <pyqtgraph.ImageItem>` for more details.
        """
        self._brush_data = brush_data
        self._brush_mask = brush_mask
        self._brush_center = brush_center
        self._brush_mode = draw_mode

        self.setDrawKernel(self._brush_data, self._brush_mask, self._brush_center, self._brush_mode)
        self._brush_set = True

    def clear_brush(self):
        '''
        Clear the brush.
        '''
        self._brush_data = None
        self._brush_mask = None
        self._brush_center = None
        self._brush_mode = None

        self.setDrawKernel()
        self._brush_set = False



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

        viewPos = self.getViewBox().mapSceneToView(ev.scenePos())
        self.onClick.emit(self, (viewPos.x(), viewPos.y()))

    def mouseDragEvent(self, ev: MouseDragEvent):
        if self.draggable != True:
            return
        ev.accept()

        viewPos = self.getViewBox().mapSceneToView(ev.scenePos())

        if ev.isStart():
            self.onDraggingBegin.emit(self, (viewPos.x(), viewPos.y()))
        elif ev.isFinish():
            self.onDraggingFinish.emit(self, (viewPos.x(), viewPos.y()))
        else:
            self.onDragging.emit(self, (viewPos.x(), viewPos.y()))
