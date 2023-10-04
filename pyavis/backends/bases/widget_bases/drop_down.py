from abc import abstractmethod
from typing import List, Any, Callable

from .widget import Widget



class BaseDropDown(Widget):
    """
    Abstract base class representing drop downs.
    """

    @abstractmethod
    def __init__(self, description: str, options: List[Any], default: Any = None):
        """
        Initalizes drop down.

        Parameters
        ----------
        description : str
            Description of the drop down.
        options : List[Any]
            Selectable options of the drop down.
        default : Any, optional
            Default value of the drop down, by default None
        """
        pass

    @abstractmethod
    def get_value(self) -> Any | None:
        """
        Return the currently selected drop down value.

        Returns
        -------
        Any | None
            The value of the drop down, or None
        """
        pass

    @abstractmethod
    def add_on_selection_changed(self, func: Callable[[int], None]):
        """
        Add a callback that is called on drop down value change.

        Parameters
        ----------
        func : Callable[[int], None]
            Function to call with index of the value
        """
        pass

    @abstractmethod
    def remove_on_selection_changed(self, func: Callable[[int], None]):
        """
        Remove a callback.

        Parameters
        ----------
        func : Callable[[int], None]
            Function to remove
        """
        pass