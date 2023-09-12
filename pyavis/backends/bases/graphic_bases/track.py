from abc import ABC, abstractmethod
from typing import Literal, Tuple

from .axis import Axis
from .graphic_element import GraphicElement
from .selection import Selection


class Track(ABC):
    def add(self, element: GraphicElement):
        '''
        Add an element to the track.

        Parameters
        ----------
        element : GraphicElement
            Element to add
        '''
        pass

    def remove(self, element: GraphicElement):
        '''
        Remove an element from the track.

        Parameters
        ----------
        element : GraphicElement
            Element to remove
        '''
        pass

    def set_selection(self, selection: Selection):
        '''
        Set the active selection.

        Parameters
        ----------
        selection : Selection
            Selection to use
        '''
        pass

    def get_selection(self) -> Selection | None:
        '''
        Get the current selection, or None if nothing is selected.

        Returns
        -------
        Selection | None
            Active selection or None
        '''
        pass

    def unset_selection(self):
        '''
        Unset the active selection. Does nothing if no selection set.
        '''
        pass

    def set_style(self, **kwargs):
        '''
        Set the color of the track.

        Parameters
        ----------
        **kwargs : any
            Keyword arguments for setting the track colors
        '''
        pass

    def allow_dragging(self, along_x: bool, along_y: bool):
        '''
        Enable or disable dragging along an axis.

        Parameters
        ----------
        along_x : bool
            Enable / Disable dragging along x axis.
        along_y : bool
            Enable / Disable dragging along y axis.
        '''
        pass

    def set_dragging_limits(self, x_limits: Tuple[int | None, int | None], y_limits: Tuple[float | None, float | None]):
        '''
        Set the limits in which the signals can be dragged.

        Parameters
        ----------
        x_limits : (int | None, int | None), default: (None, None)
            Lower and upper limit: (lower, upper)
        y_limits : (float | None, float | None), default: (None, None)
            Lower and upper limit: (lower, upper)
        '''
        pass

    def link_track(self, track: 'Track', axis: Literal["x", "y"]):
        '''
        Link either the x or y axis of the track to other track.
        None unlinks the track.

        Parameters
        ----------
        track : Track | None
            Track to link with, or None to unlink
        axis : {'x', 'y'}
            Axis to link / unlink
        '''
        pass

    def set_axis(self, axis: Axis):
        '''
        Set the axes of the track.

        Parameters
        ----------
        axis : Axis
            ...
        '''
        pass