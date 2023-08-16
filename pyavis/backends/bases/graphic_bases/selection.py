from abc import ABC
from typing import Tuple

from pyavis.shared.util import Subject


class Selection(ABC):
    def __init__(self, orientation: str, region: Tuple[float, float]):
        self.regionChanged = Subject()
        self._orientation = orientation
        self._region = region
        self._active = True

    def set_region(self, region: Tuple[float, float]):
        if self._region[0] == region[0] and self._region[1] == region[1]:
            return

        self._region = region
        self.regionChanged.emit(self, region)

    def get_region(self) -> Tuple[float, float]:
        return self._region

    def set_active(self, active: bool):
        self._active = active

    def set_style(self, style):
        pass