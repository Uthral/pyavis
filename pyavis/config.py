from typing import Tuple
from pyavis.shared.util import color


PYAVIS_DEFAULT_STYLE_CONFIG = {
    "line_color": (0.8, 0.0, 0.8),
    "border_color": (0.8, 0.8, 0.8),
    "fill_color": (0.8, 0.8, 0.8, 0.4),
    "background_color": (1.0, 1.0, 1.0)
}

def set_style_config_value(
        key: str,
        value: color.color
):
    '''
    Set configuration value.
    '''
    if key not in PYAVIS_DEFAULT_STYLE_CONFIG:
        raise KeyError(f"Unknown style configuration: '{key}'")
    
    if not isinstance(value, tuple):
        raise TypeError(f"Unknown value type: '{value}'")
    
    if len(value) != 3 and len(value) != 4:
        raise TypeError(f"value must be tuple of length '3' or '4'")
    
    color._check_color(value)
    PYAVIS_DEFAULT_STYLE_CONFIG[key] = value

def set_style_config_values(**kwargs):
    for key, value in kwargs.items():
        set_style_config_value(key, value)

def get_style_config_value(key):
    return PYAVIS_DEFAULT_STYLE_CONFIG[key]