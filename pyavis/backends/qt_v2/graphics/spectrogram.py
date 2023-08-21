from typing import Tuple

import pyqtgraph as pg
import numpy as np

from pyqtgraph.Qt import QtCore, QtWidgets

from pyavis.backends.bases.graphic_bases import Spectrogram
from pyqtgraph.GraphicsScene.mouseEvents import *


class M_SpectrogramQt(type(Spectrogram), type(pg.ImageItem)): pass
class SpectrogramQt(Spectrogram, pg.ImageItem, metaclass=M_SpectrogramQt):

    sigClicked = QtCore.Signal(object, MouseClickEvent)
    sigDragged = QtCore.Signal(object, MouseDragEvent)
    sigHovered = QtCore.Signal(object, HoverEvent)

    def __init__(self, data, size, fn):
        Spectrogram.__init__(self)
        pg.ImageItem.__init__(self)

        self.data = data
        self.size = size
        self.fn = fn

        disp = self.fn(self.data)

        self.setImage(disp.T)
        self.setRect(*self.position, *self.size)
    
    def set_size(self, size: Tuple[float, float]):
        '''
        Set the size of the spectrogram.

        Parameters
        ----------
        size : (float, float)
            New size. Format: (width, height)
        '''
        self.size = size
        self.setRect(*self.position, *self.size)

    def set_data(self, data):
        '''
        Set the data to display as spectrogram.

        Parameter
        ---------
        data : 
            Data to display as spectrogram
        '''
        self.data = data
        self.reset()

    def reset(self):
        '''
        Reset the image to the origninal :class:`Astft <pya.Astft>`
        '''
        self.setImage(self.fn(self.data).T)

    def clear(self):
        '''
        Clear spectrogram.
        '''
        self.data = None
        self.clear()

    def mouseClickEvent(self, ev: MouseClickEvent):
        if self.clickable != True:
            return
        ev.accept()
        self.sigClicked.emit(self, ev)

        self.click.emit()

    def mouseDragEvent(self, ev: MouseDragEvent):
        if self.draggable != True:
            return
        ev.accept()
        self.sigDragged.emit(self, ev)

        x,y = ev.pos().x(), ev.pos().y()
        drag_pos = (x,y)

        if ev.isStart():
            self.draggingBegin.emit(self, drag_pos)
        elif ev.isFinish():
            self.draggingFinish.emit(self, drag_pos)
        else:
            self.dragging.emit(self, drag_pos)
  
    def hoverEvent(self, ev: HoverEvent):
        self.sigHovered.emit(self, ev)