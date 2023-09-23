from typing import Callable, Any
from overrides import override
from pyqtgraph.Qt import QtWidgets, QtCore

from pyavis.backends.bases.widget_bases import BaseIntSlider, BaseFloatSlider

# from PySide2 import QtWidgets, QtCore

class IntSliderQt(BaseIntSlider):
    
    @override
    def __init__(self, description: str, orientation: str, default: int, min: int, max: int, step: int):
        super().__init__(description, orientation, default, min, max, step)
        
        if orientation == "horizontal":
            ori = QtCore.Qt.Horizontal
            self.box = QtWidgets.QHBoxLayout()
        elif orientation == "vertical":
            ori = QtCore.Qt.Vertical
            self.box = QtWidgets.QVBoxLayout()
        else:
            raise ValueError(f"{orientation} is not a valid orientation.")
        
        self.slider = _StepSlider(orientation=ori, min=min, max=max, step=step)
        self.set_value(default)

        self.text = QtWidgets.QLabel(text=description)
        self.value_text = QtWidgets.QLabel(text=str(self.get_value()))

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
        self.slider.sliderValueChanged.connect(func)

    @override
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        self.slider.sliderValueChanged.disconnect(func)

class FloatSliderQt(BaseFloatSlider):
        
    @override
    def __init__(self, description: str, orientation: str, default: float, min: float, max: float, step: float):
        super().__init__(description, orientation, default, min, max, step)

        if orientation == "horizontal":
            ori = QtCore.Qt.Horizontal
            self.box = QtWidgets.QHBoxLayout()
        elif orientation == "vertical":
            ori = QtCore.Qt.Vertical
            self.box = QtWidgets.QVBoxLayout()
        else:
            raise ValueError(f"{orientation} is not a valid orientation.")

        self.slider = _StepSlider(orientation=ori, min=min, max=max, step=step)
        self.set_value(default)

        self.text = QtWidgets.QLabel(text=description)
        self.value_text = QtWidgets.QLabel(text=str(self.get_value()))

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
    def set_value(self, value: float):
        self.slider.setValue(value)

    @override
    def get_value(self) -> float:
        return self.slider.value()

    @override
    def add_on_value_changed(self, func: Callable[[Any], None]):
        self.slider.sliderValueChanged.connect(func)

    @override
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        self.slider.sliderValueChanged.disconnect(func)

class _StepSlider(QtWidgets.QSlider):
    
    sliderValueChanged = QtCore.Signal(object)

    def __init__(
            self,
            orientation: QtCore.Qt.Orientation,
            min: int | float,
            max: int | float,
            step: int | float
    ):
        if step == 0:
            raise ValueError("0 is not a valid step size")
        
        if min > max:
            raise ValueError("min must be smaller than max")
        
        QtWidgets.QSlider.__init__(self, orientation=orientation)
        self._slider_min = min
        self._slider_max = max
        self._slider_step = step

        steps = int((self._slider_max - self._slider_min) / self._slider_step)
        super().setMaximum(steps)

        # QSlider continues to return int: Add new signal that returns custom value
        self.valueChanged.connect(self._react_to_value_change)

    @override
    def setValue(self, value):
        if value > self._slider_max:
            value = self._slider_max
        elif value < self._slider_min:
            value = self._slider_min

        # QSlider uses integers internally, adjust our value based on this
        index = round((value - self._slider_min) / self._slider_step)
        return super().setValue(index)

    @override
    def value(self) -> int | float:
        # QSlider uses integers internally, adjust value to our range & step size
        return super().value() * self._slider_step + self._slider_min
    
    def _react_to_value_change(self, _: int):
        self.sliderValueChanged.emit(self.value())
