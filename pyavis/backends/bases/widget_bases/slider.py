from abc import abstractmethod
from typing import Callable, Any
from .widget import Widget

class BaseIntSlider(Widget):
    
    @abstractmethod
    def __init__(self, description: str, orientation: str, default: int, min: int, max: int, step: int):
        self._validate_slider_values(default, min, max, step)
        self._validate_orientation(orientation)

    @abstractmethod
    def set_value(self, value: int):
        pass

    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def add_on_value_changed(self, func: Callable[[Any], None]):
        pass

    @abstractmethod
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        pass

    def _validate_slider_values(self, default: int, min: int, max: int, step: int):
        for v in [default, min, max, step]:
            if not isinstance(v, float) and not isinstance(v, int):
                raise TypeError("Values must be numbers")
        
        if int(min) > (max):
            raise ValueError("max must be larger than min")
        
        if int(default) < int(min) or int(default) > int(max):
            raise ValueError("default must be between min and max")
        
        if int(step) < 1:
            raise ValueError("step must be atleast 1")
        
    def _validate_orientation(self, orientation: str):
        if not isinstance(orientation, str):
            raise TypeError("orientation must be passed as str")
        
        if not orientation in ["horizontal", "vertical"]:
            raise ValueError("orientation must be either 'horizontal' or 'vertical'")

class BaseFloatSlider(Widget):
        
    @abstractmethod
    def __init__(self, description: str, orientation: str, default: float, min: float, max: float, step: float):
        self._validate_slider_values(default, min, max, step)
        self._validate_orientation(orientation)

    @abstractmethod
    def set_value(self, value: float):
        pass

    @abstractmethod
    def get_value(self) -> float:
        pass

    @abstractmethod
    def add_on_value_changed(self, func: Callable[[Any], None]):
        pass

    @abstractmethod
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        pass

    def _validate_slider_values(self, default: float, min: float, max: float, step: float):
        for v in [default, min, max, step]:
            if not isinstance(v, float) and not isinstance(v, int):
                raise TypeError("Values must be numbers")
        
        if float(min) > float(max):
            raise ValueError("max must be larger than min")
        
        if float(default) < float(min) or float(default) > float(max):
            raise ValueError("default must be between min and max")
        
        if float(step) <= 0:
            raise ValueError("step must be larger than 0")
        
    def _validate_orientation(self, orientation: str):
        if not isinstance(orientation, str):
            raise TypeError("orientation must be passed as str")
        
        if not orientation in ["horizontal", "vertical"]:
            raise ValueError("orientation must be either 'horizontal' or 'vertical'")

        