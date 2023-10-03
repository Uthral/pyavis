# pyavis

Visualization library for pya.

pyavis supports different backends. 

It provides a selection of widgets and data vizualization tools.

```Python
from pyavis.widgets import GraphicDisp
from pyavis.graphics import Layout

layout = Layout(1,1)
track = layout.add_track("Signal", 0, 0)
track.add_signal()

display = GraphicDisp(layout)
display.show()
```

