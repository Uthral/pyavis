from abc import ABC, abstractmethod
from typing import Callable, List, Literal, Tuple

import numpy as np
from pya import Asig, Astft

from .axis import Axis
from .graphic_element import GraphicElement
from .signal import Signal
from .rectangle import Rectangle
from .inf_line import InfLine
from .spectrogram import Spectrogram
from .rect_selection import RectSelection

class Track(ABC):
    def __init__(self, label: str):
        self._label = label
        self._axis: List[Axis] = []

    def set_x_view_limits(self, x_start, x_end):
        pass

    def set_y_view_limits(self, y_start, y_end):
        pass

    def add_signal(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            vertical_size: float | Literal["auto"] = "auto",
            *args,
            **kwargs
    ) -> Signal:
        '''
        Add a new signal to the track.

        Parameters
        ----------
        position: (float, float)
            Position of the signal
        vertical_size: float | "auto"
            New vertical size of the signal. If "auto" then use of orignal values for size.
        *args & **kwargs 
            See `Signal.set_data()` for more information.
        '''

    def add_line(
            self,
            position: Tuple[float, float]=(1.0, 1.0),
            angle: float = 0.0
    ) -> InfLine:
        '''
        Add a new infinite line to the track.

        Parameters
        ----------
        position: (float, float)
            Position of the line
        angle: float
            Angle of the line
        '''
        

    def add_rect(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            width: float = 1.0,
            height: float = 1.0
    ) -> Rectangle:
        '''
        Add a new rectangle to the track.

        Parameters:
        position: (float, float)
            Position of the rectangle. (lower-left corner)
        width: float
            Width of the rectangle
        height: float
            Heigth of the rectangle
        '''

    def add_spectrogram(        
        self, 
        data: Asig | Astft,
        position: Tuple[float, float] = (0.0, 0.0),
        scale: float = 1.0, 
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs
    ) -> Spectrogram:
        '''
        Add a new spectrogram to the track.

        Parameters
        ----------
        data: Asig | Astft
            Data to display as spectrogram
        position: (float, float)
            Position of the spectrogram
        scale: float
            Scale of the spectrogram
        disp_func: (np.ndarray) -> np.ndarray
            Function to apply to the stft data
        '''
        pass

    def add_selection(
            self,
            position: Tuple[float, float],
            size: Tuple[float, float]
    ) -> RectSelection:
        '''
        Add an adjustable selection to the track.

        Parameters
        ----------
        positon: (float, float)
            Position of the selection (bottol-left corner)
        size: (float, float)
            Size of the selection
        '''
        pass

    def remove(self, element: GraphicElement):
        '''
        Remove an element from the track.

        Parameters
        ----------
        element: GraphicElement
            Element to remove
        '''
        pass

    def set_style(self):
        pass
    
    def link_track(
            self,
            track: 'Track',
            axis: Literal["x", "y"]
    ):
        '''
        Link either x or y axis of this track with another track.

        Parameters
        ----------
        track: Track | None
            Track to link axis with. If None, the track will instead remove it's present link
        axis: 'x' or 'y'
            Axis to link
        '''
        if axis != 'x' and axis !='y':
            raise ValueError("Not a valid axis")
        
        self._link_track(track, axis)
    
    @abstractmethod
    def _link_track(self, track: 'Track', axis: Literal["x", "y"]):
        pass

    def get_axis(self, side: Literal['top', 'bottom', 'left', 'right']) -> Axis | None:
        '''
        Return the axis, or None if no axis is set for that side.

        Parameters
        ----------
        side: 'top' | 'bottom' | 'left' | 'right'
            Side to get the axis from
        '''
        v = [value for value in self._axis if value._side == side]
        return v[0] if len(v) > 0 else None
    
    def toggle_axis(self, side: Literal['top', 'bottom', 'left', 'right'], show=True):
        '''
        Hide or show the axis of the side.

        Parameters
        ----------
        side: 'top' | 'bottom' | 'left' | 'right'
            Side to toggle the axis of
        '''
        axis = self.get_axis(side)
        if axis is not None:
            axis.toggle_visibility(show)
        else:
            raise ValueError(f"Axis not set for side: {side}")
    
    def set_axis(self, side: Literal['top', 'bottom', 'left', 'right'], spacing, disp_func) -> Axis:
        '''
        Set a new axis for the choosen side. 

        Parameters
        ----------
        side: 'top' | 'bottom' | 'left' | 'right'
            Side of the new axis
        spacing: 
        '''
        pass

    def set_x_view_limits(self, x_start: float, x_end: float):
        '''
        Set the visible range of the x axis.

        Parameters
        ----------
        x_start: float
            Start of the x view range
        x_end: float
            End of the x view range
        '''
        pass

    def set_y_view_limits(self, y_start, y_end):
        '''
        Set the visible range of the y axis.

        Parameters
        ----------
        y_start: float
            Start of the y view range
        y_end: float
            End of the y view range
        '''
        pass


    