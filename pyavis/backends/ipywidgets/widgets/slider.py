from typing import Callable, Any
from pyavis.backends.bases.widget_bases import BaseFloatSlider, BaseIntSlider
from ipywidgets import IntSlider, FloatSlider

class IntSliderIPY(BaseIntSlider):
    def __init__(self, description: str, orientation: str, default: int = 50, min: int = 1, max: int = 100, step: int = 1):
        super().__init__(description, orientation, default, min, max, step)
        
        self.slider = IntSlider(
            value=default,
            min=min,
            max=max,
            step=step,
            description=description,
            orientation=orientation
        )

        self.functions = {}
        
    def get_native_widget(self):
        return self.slider
    
    def set_value(self, value: int):
        self.slider.value = value

    def get_value(self) -> int:
        return self.slider.value

    def add_on_value_changed(self, func: Callable[[Any], None]):
        internal_func = lambda x: func(x["new"])
        self.functions[func] = internal_func
        self.slider.observe(self.functions[func], 'value')

    def remove_on_value_changed(self, func: Callable[[Any], None]):
        internal_func = self.functions.pop(func)
        self.slider.unobserve(internal_func, 'value')

class FloatSliderIPY(BaseFloatSlider):
    def __init__(self, description: str, orientation: str, default: float, min: float, max: float, step: float):
        super().__init__(description, orientation, default, min, max, step)

        self.slider = FloatSlider(
            value=default,
            min=min,
            max=max,
            step=step,
            description=description,
            orientation=orientation
        )

        self.functions = {}
    
    def get_native_widget(self):
        return self.slider

    def set_value(self, value: float):
        self.slider.value = value

    def get_value(self) -> float:
        return self.slider.value
    
    def add_on_value_changed(self, func: Callable[[Any], None]):
        internal_func = lambda x: func(x["new"])
        self.functions[func] = internal_func
        self.slider.observe(self.functions[func], 'value')

    def remove_on_value_changed(self, func: Callable[[Any], None]):
        internal_func = self.functions.pop(func)
        self.slider.unobserve(internal_func, 'value')