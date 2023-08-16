from abc import ABC, abstractmethod


class Widget(ABC):
    @abstractmethod
    def get_native_widget(self):
        pass

    @abstractmethod
    def show(self):
        pass