from abc import abstractmethod
from typing import List, Any, Callable

from .widget import Widget



class BaseDropDown(Widget):

    @abstractmethod
    def __init__(self, description: str, options: List[Any], default: Any):
        pass

    @abstractmethod
    def get_value(self) -> Any | None:
        pass

    @abstractmethod
    def add_on_selection_changed(self, func: Callable[[Any], None]):
        pass

    @abstractmethod
    def remove_on_selection_changed(self, func: Callable[[Any], None]):
        pass