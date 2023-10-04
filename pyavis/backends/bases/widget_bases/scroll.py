from abc import abstractmethod
from .widget import Widget


class BaseScrollArea(Widget):
    """
    Abstract base class representing a scrollable area.
    """
    @abstractmethod
    def __init__(self, height: int = 100, width: int = 100):
        """
        Initalizes scrollable area.

        Parameters
        ----------
        height : int
            Height of the area
        width : int 
            Widgth of the area
        """
        pass

    @abstractmethod
    def set_widget(widget: Widget):
        """
        Set the widget to display in the scrollable area.

        Parameters
        ----------
        widget : Widget
            Widget to display
        """
        pass