from abc import abstractmethod
from typing import Callable, Any, Literal
from .widget import Widget

class BaseIntSlider(Widget):
    """
    Abstract base class represenitng a integer slider.
    """
    
    @abstractmethod
    def __init__(self, description: str, orientation: Literal["horizontal", "vertical"], default: int, min: int, max: int, step: int):
        """
        Initalizes integer slider.

        Parameters
        ----------
        description : str
            Description of the slider
        orientation : str
            Orientation of the slider
        default : int
            Default value of the slider
        min : int
            Minimum value of the slider
        max : int
            Maximum value of the slider
        step : int
            Step size in which the slider can be incremented
        """
        self._validate_slider_values(default, min, max, step)
        self._validate_orientation(orientation)

    @abstractmethod
    def set_value(self, value: int):
        """
        Set the value of the slider.

        Parameters
        ----------
        value : int
            Value to set
        """
        pass

    @abstractmethod
    def get_value(self) -> int:
        """
        Get the current value of the slider

        Returns
        -------
        int
            Current value of the slider
        """
        pass

    @abstractmethod
    def add_on_value_changed(self, func: Callable[[int], None]):
        """
        Add a callback that is called on slider value change.

        Parameters
        ----------
        func : Callable[[int], None]
            Function to call
        """
        pass

    @abstractmethod
    def remove_on_value_changed(self, func: Callable[[int], None]):
        """
        Remove a callback.

        Parameters
        ----------
        func : Callable[[int], None]
            Function to remove
        """
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
    """
    Abstract base class represenitng a float slider.
    """
        
    @abstractmethod
    def __init__(self, description: str, orientation: Literal["horizontal", "vertical"], default: float, min: float, max: float, step: float):
        """
        Initalizes float slider.

        Parameters
        ----------
        description : str
            Description of the slider
        orientation : str
            Orientation of the slider
        default : float
            Default value of the slider
        min : float
            Minimum value of the slider
        max : float
            Maximum value of the slider
        step : float
            Step size in which the slider can be incremented
        """
        self._validate_slider_values(default, min, max, step)
        self._validate_orientation(orientation)

    @abstractmethod
    def set_value(self, value: float):
        """
        Set the value of the slider.

        Parameters
        ----------
        value : float
            Value to set
        """
        pass

    @abstractmethod
    def get_value(self) -> float:
        """
        Get the current value of the slider

        Returns
        -------
        float
            Current value of the slider
        """
        pass

    @abstractmethod
    def add_on_value_changed(self, func: Callable[[float], None]):
        """
        Add a callback that is called on slider value change.

        Parameters
        ----------
        func : Callable[[float], None]
            Function to call
        """
        pass

    @abstractmethod
    def remove_on_value_changed(self, func: Callable[[float], None]):
        """
        Remove a callback.

        Parameters
        ----------
        func : Callable[[float], None]
            Function to remove
        """
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

        