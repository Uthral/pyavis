from typing import Callable, List, Any
from overrides import override
from pyavis.backends.bases.widget_bases import BaseDropDown
from ipywidgets import Dropdown

class DropDownIPY(BaseDropDown):

    @override
    def __init__(self, description: str, options: List[Any], default: Any = None):
        self.drop_down = Dropdown(
            description=description,
            options=options,
            value=default if default is not None else options[0]
        )

    @override
    def get_native_widget(self):
        return self.drop_down
    
    @override
    def get_value(self) -> Any | None:
        return self.drop_down.value
    
    @override
    def add_on_selection_changed(self, func: Callable[[int], None]):
        self.drop_down.observe(lambda x: func(x['owner'].index), names="value")

    @override
    def remove_on_selection_changed(self, func: Callable[[int], None]):
        self.drop_down.unobserve(func, names="value")