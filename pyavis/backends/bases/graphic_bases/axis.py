from abc import ABC, abstractmethod
from typing import Callable, Tuple


class Axis(ABC):
    @abstractmethod
    def set_disp_func(self, func: Callable[[float], str]):
        '''
        Set the display function, that converts between axis value and axis display text.

        Parameters
        ----------
        func : (float) -> str
            Convert axis value to axis display text
        '''
        pass
    
    @abstractmethod
    def set_spacing(self, spacing: Tuple[float, float]=None):
        '''
        Set distance of minor and major ticks.

        Paramters
        ---------
        spacing : (float, float) | None, default: None
            Set the spacing between ticks. Format: (major, minor).
            If None, uses default value.
        '''
        pass