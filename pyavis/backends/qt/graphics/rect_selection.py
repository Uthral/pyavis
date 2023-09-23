from pyavis.backends.bases.graphic_bases import RectSelection

import pyqtgraph as pg
from pyqtgraph.GraphicsScene.mouseEvents import *

class M_RectSelectionQt(type(RectSelection), type(pg.ROI)): pass
class RectSelectionQt(RectSelection, pg.ROI, metaclass=M_RectSelectionQt):
    def __init__(
            self,
            pos,
            width,
            height
    ):
        RectSelection.__init__(self, pos, (width, height))
        pg.ROI.__init__(self, pos, (width, height))

        # Disable default pyqtgraph interaction of ROI
        self.translatable = False
        self.resizable = False
        self.rotatable = False
        self.removable = False

        self._region_change_func = lambda x: self._region_changed_callback(x)
        self._handle_callback_connections(True)

    def add_handle(self, side: str, mirror: bool = False):
        if side == "left":
            center = [1.0, 0.5] if not mirror else [0.5, 0.5]
            pos = [0.0, 0.5]
        elif side == "right":
            center = [0.0, 0.5] if not mirror else [0.5, 0.5]
            pos = [1.0, 0.5]
        elif side == "top":
            center = [0.5, 0.0] if not mirror else [0.5, 0.5]
            pos = [0.5, 1.0]
        elif side == "bottom":
            center = [0.5, 1.0] if not mirror else [0.5, 0.5]
            pos = [0.5, 0.0]
        else:
            raise ValueError(f"'{side}' is not a valid orientation, 'side' must be 'left', 'right', 'top' or 'bottom'.")

        if side in self._handles.keys():
            self.removeHandle(self._handles[side])

        h = self.addScaleHandle(pos, center)
        self._handles[side] = h
    
    def remove_handle(self, side: str):
        if side not in ["left", "right", "top", "bottom"]:
            raise ValueError(f"'{side}' is not a valid orientation, 'side' must be 'left', 'right', 'top' or 'bottom'.")
        
        if side not in self._handles.keys():
            raise KeyError(f"No handle for side '{side}' to remove.")
        
        self.removeHandle(self._handles[side])
        del self._handles[side]


    def _abstract_set_active(self):
        if self.active:
            self.show()
        else:
            self.hide()
    
    def _abstract_set_position(self):
        self._handle_callback_connections(False)
        self.setPos(self.position)
        self._handle_callback_connections(True)

    def _abstract_set_size(self):
        self._handle_callback_connections(False)
        self.setSize(self.size)
        self._handle_callback_connections(True)

    def _handle_callback_connections(self, connect: bool):
        '''
        Connect or disconnect callbacks.
        Used to keep base class in sync
        '''
        if connect:
            self.sigRegionChangeStarted.connect(self._region_change_func)
            self.sigRegionChanged.connect(self._region_change_func)
            self.sigRegionChangeFinished.connect(self._region_change_func)
        else:
            self.sigRegionChangeStarted.disconnect(self._region_change_func)
            self.sigRegionChanged.disconnect(self._region_change_func)
            self.sigRegionChangeFinished.disconnect(self._region_change_func)


    def _region_changed_callback(self, s: 'RectSelectionQt'):
        '''
        Update pyavis base-class after interacting with the handles.
        '''
        old_position = self.position
        old_size = self.size

        pos = s.state["pos"]
        size = s.state["size"]

        self._internal_set_position(pos[0], pos[1])
        self._internal_set_size((size[0], size[1]))

        self.positionChanged.emit(self, self.position, old_position)
        self.sizeChanged.emit(self, self.size, old_size)


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



    def _abstract_set_style(self, line_color, handle_color):
        from pyavis.shared.util import color
        line_color = color._convert_color(line_color)
        handle_color = color._convert_color(handle_color)
        
        self.setPen(pg.mkPen(pg.mkColor(*line_color), width=0))
        self.handlePen = pg.mkPen(pg.mkColor(*handle_color), width=0)
        