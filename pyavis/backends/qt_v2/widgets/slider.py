from typing import Callable, Any
from overrides import override
from pyqtgraph.Qt import QtWidgets, QtCore

from pyavis.backends.bases.widget_bases import BaseIntSlider, BaseFloatSlider

class IntSliderQt(BaseIntSlider):
    
    @override
    def __init__(self, description: str, orientation: str, default: int, min: int, max: int, step: int):
        self.text = QtWidgets.QLabel(text=description)
        self.value_text = QtWidgets.QLabel(text=str(default))
        
        if orientation == "horizontal":
            ori = QtCore.Qt.Horizontal
            self.box = QtWidgets.QHBoxLayout()
        elif orientation == "vertical":
            ori = QtCore.Qt.Vertical
            self.box = QtWidgets.QVBoxLayout()
        else:
            raise ValueError(f"{orientation} is not a valid orientation.")
        
        self.slider = QtWidgets.QSlider(orientation=ori)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(default)
        self.slider.setSingleStep(step)

        #TODO: Add step

        self.box.addWidget(self.text)
        self.box.addWidget(self.slider)
        self.box.addWidget(self.value_text)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.box)

        self.add_on_value_changed(lambda x: self.value_text.setText(str(x)))
        
    @override
    def get_native_widget(self):
        return self.widget

    @override
    def set_value(self, value: int):
        self.slider.setValue(value)

    @override
    def get_value(self) -> int:
        return self.slider.value()

    @override
    def add_on_value_changed(self, func: Callable[[Any], None]):
        self.slider.valueChanged.connect(func)
        pass

    @override
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        self.slider.valueChanged.disconnect(func)
        pass

class FloatSliderQt(BaseFloatSlider):
        
    @override
    def __init__(self, description: str, orientation: str, default: float, min: float, max: float, step: float):
        pass

    @override
    def get_native_widget(self):
        return self.widget

    @override
    def set_value(self, value: float):
        pass

    @override
    def get_value(self) -> float:
        pass

    @override
    def add_on_value_changed(self, func: Callable[[Any], None]):
        pass

    @override
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        pass