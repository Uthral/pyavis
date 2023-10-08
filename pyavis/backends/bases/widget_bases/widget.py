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
    def show(self, *args, **kwargs):
        """
        Display the widget.

        Parameters
        ----------
        **exec: bool, optional
            Used by Qt-based backend if used outside of interactive environment to delay start of QApplication.
            Set to True for last `show()` invocation to start QApplication, by default False.
        """
        pass