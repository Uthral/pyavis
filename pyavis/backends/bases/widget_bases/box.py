from abc import abstractmethod
from .widget import Widget


class BaseVBox(Widget):
    """
    Abstract base class representing a widget for vertical layouting.
    """

    @abstractmethod
    def add_widget(self, widget: Widget):
        """
        Add a widget to the box.

        Parameters
        ----------
        widget : Widget
            Widget to add
        """
        pass

    @abstractmethod
    def remove_widget(self, widget: Widget):
        """
        Remove a widget from the box.

        Parameters
        ----------
        widget : Widget
            Widget to remvoe
        """
        pass

class BaseHBox(Widget):
    """
    Abstract base class representing a widget for horizontal layouting.
    """

    @abstractmethod
    def add_widget(self, widget: Widget):
        """
        Add a widget to the box.

        Parameters
        ----------
        widget : Widget
            Widget to add
        """
        pass

    @abstractmethod
    def remove_widget(self, widget: Widget):
        """
        Remove a widget from the box.

        Parameters
        ----------
        widget : Widget
            Widget to remvoe
        """
        pass