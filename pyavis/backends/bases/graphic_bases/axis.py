from abc import ABC, abstractmethod
from typing import Callable, Tuple


class Axis(ABC):
    @abstractmethod
    def set_disp_func(self, func: Callable[[float], str]):
        pass
    
    @abstractmethod
    def set_spacing(self, spacing: Tuple[float, float]=None):
        pass