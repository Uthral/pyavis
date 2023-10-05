from typing import Callable, Tuple
from pya import Asig, Aspec
from pyavis.backends.bases.graphic_bases.spectrum import Spectrum

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.GraphicsScene.mouseEvents import *

import numpy as np

class M_SpectrumQt(type(Spectrum), type(pg.GraphicsObject)): pass
class SpectrumQt(Spectrum, pg.GraphicsObject, metaclass=M_SpectrumQt):
    def __init__(        
        self,
        data: Asig | Aspec,
        position: Tuple[float, float] = (0.0, 0.0),
        scale: float = 1.0, 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
    ):
        Spectrum.__init__(self, data, position, scale, disp_func)
        pg.GraphicsObject.__init__(self)
        
        self.signal = pg.PlotDataItem()
        self.signal.setParentItem(self)

        self.set_style("default")
        self._update_plot()

    def _update_plot(self):
        self.signal.setData(
            x=self.orig_spec.freqs + self.position[0],
            y=self.disp_func(self.orig_spec.rfftspec) * self.scale + self.position[1]
        )

    def _abstract_set_active(self):
        if self.active:
            self.show()
        else:
            self.hide()
    
    def _abstract_set_data(self):
        self._update_plot()
    
    def _abstract_set_position(self):
        self._update_plot()
    
    def _abstract_set_scale(self):
        self._update_plot()

    def _abstract_set_style(self, line_color):
        from pyavis.shared.util import color
        line_color = color._convert_color(line_color)
        self.signal.setPen(pg.mkPen(pg.mkColor(*line_color), width=0))


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

    def boundingRect(self):
        return self.signal.curve.boundingRect()