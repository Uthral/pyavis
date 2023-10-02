import typing

class Subject:
    def __init__(self):
        self.observers: typing.List[typing.Callable] = []

    def connect(self, observer: typing.Callable):
        self.observers.append(observer)

    def disconnect(self, observer: typing.Callable):
        self.observers.remove(observer)

    def emit(self, *arguments : typing.Any):
        for observer in self.observers:
            observer(*arguments)

    def clear(self):
        self.observers = []