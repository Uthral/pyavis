from abc import ABC, abstractmethod
from typing import Any, Callable, List, Literal, Tuple

import numpy as np
from pya import Asig, Astft

from .axis import Axis
from .graphic_element import GraphicElement
from .signal import Signal
from .rectangle import Rectangle
from .infinite_line import InfiniteLine
from .spectrogram import Spectrogram
from .rect_selection import RectSelection

class Track(ABC):
    def __init__(self, label: str):
        self._label = label
        self._axis: List[Axis] = []

    def add_signal(
            self,
            position: Tuple[float, float] = (0.0, 0.0),
            scale: float = 1.0,
            *args,
            **kwargs
    ) -> Signal:
        '''
        Add a new signal to the track.

        Parameters
        ----------
        position: (float, float)
            Position of the signal
        scale: float
            Scale of the y values, by default 1.0
        *args & **kwargs 
            See `Signal.set_data()` for more information.
        '''

    def add_line(
            self,
            position: Tuple[float, float]=(1.0, 1.0),
            angle: float = 0.0
    ) -> InfiniteLine:
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
        disp_func: Callable[[np.ndarray], np.ndarray] = np.abs,
        with_bar: bool = True,
    ) -> Spectrogram:
        '''
        Add a new spectrogram to the track.

        Parameters
        ----------
        data: Asig | Astft
            Data to display as spectrogram
        position: (float, float)
            Position of the spectrogram
        disp_func: (np.ndarray) -> np.ndarray
            Function to apply to the stft data
        with_bar: bool
            Optional color bar added to the plot
        '''
        pass

    def add_selection(
            self,
            pos: Tuple[float, float],
            width: float,
            height: float,
    ) -> RectSelection:
        '''
        Add an adjustable selection to the track.

        Parameters
        ----------
        positon: (float, float)
            Position of the selection (bottom-left corner)
        width: float
            Width of the selection
        height: float
            Height of the selection
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
    
    def set_axis(
            self,
            side: Literal['top', 'bottom', 'left', 'right'],
            spacing: Tuple[float, float]=None,
            disp_func: Callable[[float], str]=None
    ) -> Axis:
        '''
        Set a new axis for the choosen side. 

        Parameters
        ----------
        side: 'top' | 'bottom' | 'left' | 'right'
            Side of the new axis
        spacing: (float, float) | None:
            Default spacing if None, else (major, minor) spacing
        disp_func: (float) -> str | None,
            Default displace function if None, else function values. 
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




    def set_style(self, background_color: Any | Literal["default"]):
        '''
        Set the background color of the layout.

        Parameters
        ----------
        background_color : color.color | str, default: "default"
            Either "default" or values of the format 'color.color'
        '''
        if background_color == "default":
            from pyavis.config import get_style_config_value
            background_color = get_style_config_value("background_color")
        else:
            from pyavis.shared.util import color
            color._check_color(background_color)

        self._abstract_set_style(background_color)
    
    def _abstract_set_style(self, background_color):
        pass


    