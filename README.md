# pyavis

Visualization library for pya. It provides a selection of widgets and data vizualization tools.

## Installation

`pyavis` supports different backends for visualization and widgets. Currently only a Qt- and an ipywidgets-based backend are supported. You can either install the dependencies for both backends or choose the one you want to use.

```
pip install .
pip install .[ipywidgets] 
pip install .[qt]
pip install .[full]
```

`pyavis` uses `PyQt5` as a dependencies when installed via `[qt]`, but you can manually install any other version instead, e.g. `PyQt6`.

## Simple examples

### Displaying a signal via Qt or ipywidgets / matplotlib

```Python
%gui qt # %matplotlib widget

import numpy as np
from pyavis.widgets import GraphicDisp
from pyavis.graphics import Layout
from pyavis import use_backend

use_backend("qt") # use_backend("ipywidgets")

signal = np.sin(2 * np.pi * 200 * np.linspace(0, 1, 44100))

layout = Layout(1,1)
track = layout.add_track("Signal", 0, 0)
track.add_signal((0,0), 1, signal)

display = GraphicDisp()
display.set_displayed_item(layout)
display.show()
```

### Displaying a signal via Qt in non-interactive environment

```Python
import numpy as np
from pyavis.widgets import GraphicDisp
from pyavis.graphics import Layout
from pyavis import use_backend

use_backend("qt")

signal = np.sin(2 * np.pi * 200 * np.linspace(0, 1, 44100))

layout = Layout(1,1)
track = layout.add_track("Signal", 0, 0)
track.add_signal((0,0), 1, signal)

display = GraphicDisp()
display.set_displayed_item(layout)
display.show(exec=True) # Use exec to start Qt event loop.
```
