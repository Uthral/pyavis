from abc import ABC
from typing import Any, Literal

from pyavis.shared.util import Subject
from .track import Track

class Layout(ABC):
    """
    Abstract base class representing a graphical layout.
    """
    def __init__(self, rows: int = 1, columns: int = 1):
        """
        Initalizes a layout.

        Parameters
        ----------
        rows : int, optional
            Amount of rows, by default 1
        columns : int, optional
            Amount of columns, by default 1
        """
        self.trackAdded = Subject()
        self.trackRemoved = Subject()

        self.__rows = rows
        self.__columns = columns

    @property
    def layout_rows(self) -> int:
        return self.__rows
    
    @property
    def layout_columns(self) -> int:
        return self.__columns
    
    def add_track(self, label: str, row: int, column: int, rowspan: int = 1, colspan: int = 1) -> Track:
        """
        Add a new track to the layout occupying the spacified range.

        Parameters
        ----------
        label : str
            Label of the track
        row : int
            Start row
        column : int
            Start column
        rowspan : int, optional
            Row size, by default 1
        colspan : int, optional
            Column size, by default 1

        Returns
        -------
        Track
            Newly added track

        Raises
        ------
        ValueError
            Raises if start position or span leads to incorrect area.
        """
        if row > self.layout_rows or row < 0:
            raise ValueError("Out of bounds.")
        
        if column > self.layout_columns or column < 0:
            raise ValueError("Out of bounds.")
        
        if rowspan < 1 or (row + rowspan) > self.layout_rows:
            raise ValueError("Invalid span.")
        
        if colspan < 1 or (column + colspan) > self.layout_columns:
            raise ValueError("Invalid span.")
        
        return self._add_track(label, row, column, rowspan, colspan)
    
    def remove_track(self, track: Track):
        """
        Remove track from layout.

        Parameters
        ----------
        track : Track
            Track to remove
        """
        pass

    def set_style(self, background_color: Any | Literal["default"]):
        """
        Set the background color of the layout.

        Parameters
        ----------
        background_color : color | "default"
            Either "default" or color values
        """
        if background_color == "default":
            from pyavis.config import get_style_config_value
            background_color = get_style_config_value("background_color")
        else:
            from pyavis.shared.util import color
            color._check_color(background_color)

        self._abstract_set_style(background_color)
    
    def _add_track(self, label: str, row: int, column: int, rowspan: int = 1, colspan: int = 1) -> Track:
        pass

    def _abstract_set_style(self, background_color: Any):
        pass
