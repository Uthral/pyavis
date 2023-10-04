from abc import abstractmethod
from .widget import Widget
from ..graphic_bases import Layout

class BaseGraphicDisp(Widget):
    """
    Abstract base class representing a widget to display pyavis's graphics.
    """
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def set_displayed_item(self, item: Layout):
        """
        Set the layout graphic item to display.

        Parameters
        ----------
        item : Layout
            Layout to display
        """
        pass