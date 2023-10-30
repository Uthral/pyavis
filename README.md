# pyavis

Visualization library for pya. It provides a selection of widgets and data vizualization tools.

* Documentation: see examples folder for usage examples and [Documentation](https://uthral.github.io/pyavis/index.html)
* Source code: https://github.com/Uthral/pyavis

pyavis provides:

* different backends to support different environments
* visualizations of pya datatypes (signal, spectrum and spectrogram) and more
* selection of widgets
* interactions with visualizations 

It can be used for

* visualization of audio data
* exploration of audio data
* interface development for interactions with audio data

## Installation

`pyavis` supports different backends for visualization and widgets, with different levels of interactivity. Currently only a Qt- and an ipywidgets-based backend are supported. You can either install the dependencies for both backends or choose the one you want to use.

```
pip install .
pip install .[ipywidgets] 
pip install .[qt]
pip install .[full]
```

`pyavis` uses `PyQt5` as a dependencies when installed via `[qt]`, but you can manually install any other version instead, e.g. `PyQt6`.

## Simple examples

### Displaying a signal and widgets via Qt or ipywidgets / matplotlib

```Python


import numpy as np
from pyavis.widgets import GraphicDisp
from pyavis.graphics import Layout
from pyavis import use_backend

signal = np.sin(2 * np.pi * 200 * np.linspace(0, 1, 44100)) # Values to display

%gui qt # or alternatively: %matplotlib widget
use_backend("qt") # Use qt backend to create widgets and graphcis, alternatively: use_backend("ipywidgets")

layout = Layout(1,1) # Create layout 
track = layout.add_track("Signal", 0, 0) # Add plot to layout
signal = track.add_signal((0,0), 1, signal) # Add values to plot

display = GraphicDisp() # Create widget to display layout 
display.set_displayed_item(layout)
display.show()
```

### Displaying a signal via Qt in non-interactive environment via Qt

```Python
display.show(exec=True) # Use exec to start Qt event loop.
```

### Using widgets

`pyavis` provides a selection of widgets, e.g.

```Python
from pyavis.widgets import ScrollArea, VBox, HBox, Button, ToggleButton, DropDown, IntSlider, FloatSlider, Toolbar

drop_down = DropDown(description="Test", options=["A","B","C"], default="A")
drop_down.add_on_selection_changed(lambda option: print(option))

slider = IntSlider("Slider Test", "horizontal", min=1, max=3, default=2, step=1)
slider.add_on_value_changed(lambda value: print(value))

hbox = HBox()
hbox.add_widget(drop_down)
hbox.add_widget(slider)
hbox.show()

```

### Styling elements

Most graphical items to be styled, e.g.

```Python
signal.set_style((255, 255, 255))
```

3- and 4-dimensional tuples of integers between 0 - 255 and floating point numbers between 0.0 - 1.0 are supported.

### Interacting with elements

Use `Subject`s to interact with created elements, e.g.

```Python
signal.onClick.connect(lambda element, pos: element.set_style((0, 0, 255))) # Add callbacks to execute code on event
```

### Learning more
* Please check the notebooks in examples/ for more examples and.