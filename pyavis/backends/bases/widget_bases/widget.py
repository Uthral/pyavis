from abc import ABC, abstractmethod


class Widget(ABC):
    """
    Base class for all widgets.
    """
    @abstractmethod
    def get_native_widget(self):
        """
        Return the native element of the backend underlying the widget.
        """
        pass

    @abstractmethod
    def show(self):
        """
        Display the widget.
        """
        pass