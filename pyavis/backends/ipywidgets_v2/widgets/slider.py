from typing import Callable, Any
from overrides import override
from pyavis.backends.bases.widget_bases import BaseFloatSlider, BaseIntSlider
from ipywidgets import IntSlider, FloatSlider

class IntSliderIPY(BaseIntSlider):
    @override
    def __init__(self, description="IntSlider", orientation: str = "horizontal", default: int = 50, min: int = 1, max: int = 100, step: int = 1, *args, **kwargs):
        self.slider = IntSlider(
            value=default,
            min=min,
            max=max,
            step=step,
            description=description,
            orientation=orientation
        )
        
    @override
    def get_native_widget(self):
        return self.slider
    
    @override
    def set_value(self, value: int):
        self.slider.value = value

    @override
    def get_value(self) -> int:
        return self.slider.value

    @override
    def add_on_value_changed(self, func: Callable[[Any], None]):
        self.slider.observe(func, 'value')

    @override
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        self.slider.unobserve(func, 'value')

class FloatSliderIPY(BaseFloatSlider):
    @override
    def __init__(self, description: str, orientation: str, default: float, min: float, max: float, step: float):
            self.slider = FloatSlider(
            value=default,
            min=min,
            max=max,
            step=step,
            description=description,
            orientation=orientation
        )
    
    @override
    def get_native_widget(self):
        return self.slider

    @override
    def set_value(self, value: float):
        self.slider.value = value

    @override
    def get_value(self) -> float:
        return self.slider.value

    @override
    def add_on_value_changed(self, func: Callable[[Any], None]):
        self.slider.observe(func, 'value')

    @override
    def remove_on_value_changed(self, func: Callable[[Any], None]):
        self.slider.unobserve(func, 'value')