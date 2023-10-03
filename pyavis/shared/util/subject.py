from typing import Callable, List, Any

class Subject:
    """
    Class to allow notification of subscribers.
    Simple implementation of the observer pattern.
    """
    def __init__(self):
        self.observers: List[Callable] = []

    def connect(self, observer: Callable):
        """
        Add a new subscriber to be notified on :func:``Subject.emit()`

        Parameters
        ----------
        observer : Callable
            Function to called on :func:``Subject.emit()`
        """
        self.observers.append(observer)

    def disconnect(self, observer: Callable):
        """
        Remove a subscriber.

        Parameters
        ----------
        observer : Callable
            Function to be removed
        """
        self.observers.remove(observer)

    def emit(self, *arguments):
        """
        Call all subscribers with the passed arguements.

        Parameters
        ----------
        *args
            Arguments that are passed to all subscribers
        """
        for observer in self.observers:
            observer(*arguments)

    def clear(self):
        """
        Remove all subscribers
        """
        self.observers = []