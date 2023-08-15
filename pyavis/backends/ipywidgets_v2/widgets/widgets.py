from typing import Callable, List, Any
from overrides import override
from pyavis.base_classes import BaseButton, BaseFloatSlider, BaseIntSlider, BaseDropDown, BaseScrollArea, BaseVBox, Widget, BaseHBox
from ipywidgets import Button, VBox, HBox, IntSlider, FloatSlider, Dropdown, Layout

class ButtonIPY(BaseButton):
    @override
    def __init__(self, label: str):
        self.button = Button(description=label)
    
    @override
    def get_native_widget(self):
        return self.button

    @override
    def add_on_click(self, func: Callable):
        self.button.on_click(func)
    
    def remove_on_click(self, func: Callable):
        self.button.on_click(func, remove=True)

class VBoxIPY(BaseVBox):
    def __init__(self, *args, **kwargs):
        self.vbox = VBox()
    
    @override
    def add_widget(self, widget: Widget):
        self.vbox.children += (widget.get_native_widget(),)

    @override
    def remove_widget(self, widget: Widget):
        children = list(self.vbox.children)
        children.remove(widget.get_native_widget())
        self.vbox.children = tuple(children)

    @override
    def get_native_widget(self):
        return self.vbox
    
class HBoxIPY(BaseHBox):
    def __init__(self, *args, **kwargs):
        self.hbox = HBox()
    
    @override
    def add_widget(self, widget: Widget):
        self.hbox.children += (widget.get_native_widget(),)

    @override
    def remove_widget(self, widget: Widget):
        children = list(self.hbox.children)
        children.remove(widget.get_native_widget())
        self.hbox.children = tuple(children)

    @override
    def get_native_widget(self):
        return self.hbox
    
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

class DropDownIPY(BaseDropDown):

    @override
    def __init__(self, description: str, options: List[Any], default: Any):
        self.drop_down = Dropdown(
            description=description,
            options=options,
            value=default
        )

    @override
    def get_native_widget(self):
        return self.drop_down
    
    @override
    def get_value(self) -> Any | None:
        return self.drop_down.value
    
    @override
    def add_on_selection_changed(self, func: Callable[[Any], None]):
        self.drop_down.observe(func, names="value")

    @override
    def remove_on_selection_changed(self, func: Callable[[Any], None]):
        self.drop_down.unobserve(func, names="value")

class ScrollAreaIPY(BaseScrollArea):
    @override
    def __init__(self, height: str = '250px'):
        self.scroll = None
        self.height = height

    @override
    def get_native_widget(self):
        return self.scroll

    @override
    def set_widget(self, widget: Widget):
        self.scroll = HBox([widget.get_native_widget()], layout=Layout(height=self.height, overflow='scroll', display='inline-block'))