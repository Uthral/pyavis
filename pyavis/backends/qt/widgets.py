from typing import Callable, List, Any
from overrides import override

from pyavis.base_classes import Widget
from ...base_classes import BaseButton, BaseDropDown, BaseFloatSlider, BaseIntSlider, BaseScrollArea, BaseVBox, Widget, BaseHBox
from pyqtgraph.Qt import QtWidgets, QtCore

class ButtonQt(BaseButton):
    def __init__(self, label: str):
        self.button = QtWidgets.QPushButton(text=label)
    
    @override
    def get_native_widget(self):
        return self.button
    
    @override
    def add_on_click(self, func: Callable):
        self.button.clicked.connect(func)
    
    @override
    def remove_on_click(self, func: Callable):
        self.button.clicked.disconnect(func)

class VBoxQt(BaseVBox):
    def __init__(self, *args, **kwargs):
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()

        self.widget.setLayout(self.vbox)
    
    @override
    def add_widget(self, widget: Widget):
        self.vbox.addWidget(widget.get_native_widget())

    @override
    def remove_widget(self, widget: Widget):
        self.vbox.removeWidget(widget.get_native_widget())

    @override
    def get_native_widget(self):
        return self.widget
    
class HBoxQt(BaseHBox):
    def __init__(self, *args, **kwargs):
        self.widget = QtWidgets.QWidget()
        self.hbox = QtWidgets.QHBoxLayout()

        self.widget.setLayout(self.hbox)
    
    @override
    def add_widget(self, widget: Widget):
        self.hbox.addWidget(widget.get_native_widget())

    @override
    def remove_widget(self, widget: Widget):
        self.hbox.removeWidget(widget.get_native_widget())

    @override
    def get_native_widget(self):
        return self.widget
    
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

class DropDownQt(BaseDropDown):

    @override
    def __init__(self, description: str, options: List[Any], default: Any):
        self.text = QtWidgets.QLabel(text=description)
        self.drop_down = QtWidgets.QComboBox()

        for option in options:
            if isinstance(option, str):
                self.drop_down.addItem(option)
            else:
                self.drop_down.addItem(str(option))
        idx = options.index(default)
        self.drop_down.setCurrentIndex(idx)


        self.box = QtWidgets.QHBoxLayout()
        self.box.addWidget(self.text)
        self.box.addWidget(self.drop_down)
        
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.box)

    @override
    def get_native_widget(self):
        return self.widget

    @override
    def get_value(self) -> Any | None:
        return self.drop_down.currentData()

    @override
    def add_on_selection_changed(self, func: Callable[[Any], None]):
        self.drop_down.currentIndexChanged.connect(func)

    @override
    def remove_on_selection_changed(self, func: Callable[[Any], None]):
        self.drop_down.currentIndexChanged.disconnect(func)


class ScrollAreaQt(BaseScrollArea):
    def __init__(self):
        self.scroll = QtWidgets.QScrollArea()
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.widget)

        self.scroll.setWidget(self.widget)
        self.scroll.setWidgetResizable(True)

    def set_widget(self, widget: Widget):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        w = widget.get_native_widget()
        self.layout.addWidget(w)

    @override
    def get_native_widget(self):
        return self.scroll