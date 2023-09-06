from abc import ABC, abstractmethod

from pyavis.shared.util import Subject
from .track import Track

class Layout(ABC):
    def __init__(self, rows: int = 1, columns: int = 1):
        self.layoutChanged = Subject()
        self.trackAdded = Subject()
        self.trackRemoved = Subject()

        self.__rows = rows
        self.__columns = columns

    @property
    def layout_rows(self) -> int:
        return self.__rows
    
    # @layout_rows.setter
    # def layout_rows(self, value: int):
    #     if value < 1:
    #         raise ValueError("There cannot be fewer than 1 row.")
    #     self.__rows = value
    
    @property
    def layout_columns(self) -> int:
        return self.__columns
    
    # @layout_columns.setter
    # def layout_columns(self, value: int):
    #     if value < 1:
    #         raise ValueError("There cannot be fewer than 1 column.")
    #     self.__columns = value
    
    def add_track(self, label: str, row: int, column: int, rowspan: int = 1, colspan: int = 1) -> Track:
        if row > self.layout_rows or row < 0:
            raise ValueError("Out of bounds.")
        
        if column > self.layout_columns or column < 0:
            raise ValueError("Out of bounds.")
        
        if rowspan < 1 or (row + rowspan) > self.layout_rows:
            raise ValueError("Invalid span.")
        
        if colspan < 1 or (column + colspan) > self.layout_columns:
            raise ValueError("Invalid span.")
        
        return self._add_track(label, row, column, rowspan, colspan)
    
    @abstractmethod
    def _add_track(self, label: str, row: int, column: int, rowspan: int = 1, colspan: int = 1) -> Track:
        pass
    
    def remove_track(self, track):
        pass
        
    # @abstractmethod
    # def _handle_layout_change(self):
    #     pass

