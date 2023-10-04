from abc import abstractmethod
from typing import Callable, Any
from .widget import Widget

from pyavis.shared.util.subject import Subject

class BaseButton(Widget):
    """
    Abstarct base class representing a button.
    """

    @abstractmethod
    def __init__(self, label: str):
        """
        Initalizes button.

        Parameters
        ----------
        label : str
            Label of the button
        """
        pass

    @abstractmethod
    def add_on_click(self, func: Callable):
        """
        Add a callback that is called on button click.

        Parameters
        ----------
        func : Callable
            Function to call
        """
        pass

    @abstractmethod
    def remove_on_click(self, func: Callable):
        """
        Remove a callback.

        Parameters
        ----------
        func : Callable
            Function to remove
        """
        pass

class BaseToggleButton(Widget):
    """
    Abstract base class representing a toggable button.
    """

    @abstractmethod
    def __init__(self, label: str, icon: Any = None, default_toggle_state: bool = False):
        """
        Initalizes toggable button.

        Parameters
        ----------
        label : str
            Label of the button
        icon : Any, optional
            Icon of the button, by default None. Has to be specified
        default_toggle_state : bool, optional
            Default state of the button, by default False
        """
        pass

    @abstractmethod
    def add_on_toggle(self, func: Callable):
        """
        Add a callback that is called on button toggle.

        Parameters
        ----------
        func : Callable
            Function to call
        """
        pass

    @abstractmethod
    def remove_on_toggle(self, func: Callable):
        """
        Remove a callback.

        Parameters
        ----------
        func : Callable
            Function to remove
        """
        pass