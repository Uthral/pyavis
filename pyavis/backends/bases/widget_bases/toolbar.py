from abc import abstractmethod
from typing import Callable, Any, List
from .widget import Widget

class BaseToolbar(Widget):
    """
    Abstract base class represenitng a toolbar.
    """
    @abstractmethod
    def __init__(self, labels: List[str], values: List[str]):
        """
        Initalizes toolbar.

        Parameters
        ----------
        labels : List[str]
            Labels of the toolbar buttons
        values : List[str]
            Values of the toolbar buttons

        Raises
        ------
        RuntimeError
            Raises if labels and values have different lengths
        """
        if len(labels) != len(values):
            raise RuntimeError("labels and values need the same length")
        
        self.labels = labels
        self.values = values

        self.mapping = {}
        for label, value in zip(self.labels, self.values):
            self.mapping[label] = value

    @abstractmethod
    def get_active_value(self) -> str:
        """
        Return the value of the currently active toolbar button.

        Returns
        -------
        str
            Current value of the toolbar
        """
        pass
    
    @abstractmethod
    def add_on_active_changed(self, func: Callable):
        """
        Add a callback that will be called when the active toolbar button changed.

        Parameters
        ----------
        func : Callable
            Function to call on change
        """
        pass
    
    @abstractmethod
    def remove_on_active_changed(self, func: Callable):
        """
        Remove a callback

        Parameters
        ----------
        func : Callable
            Function to remvoe
        """
        pass
