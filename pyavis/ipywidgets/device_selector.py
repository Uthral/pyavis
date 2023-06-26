import ipywidgets as widgets
from pya import *
from typing import Callable

from pyavis.shared import getInOutDevices, DeviceInfo

class DeviceSelector(widgets.VBox, widgets.Widget):
    def __init__(self, callback: Callable[[DeviceInfo], None] = None):
        super(DeviceSelector, self).__init__()
        (input_list, output_list) = getInOutDevices()
        self.input_devices = input_list
        self.output_devices = output_list
        self.callback = callback

        label = widgets.Label("Select Output Device")
        select_layout = widgets.Layout(width='max-content')
        self.select = widgets.Select(
            options=[ device.as_output_str() for device in self.output_devices ],
            disabled=False,
            row=5,
            layout=select_layout
        )
        self.output = widgets.Output()
        self.select.observe(self.on_value_change, names='index')

        box = widgets.Box([label, self.select])
        self.children = [widgets.HTML("<style>select, input { font-family: monospace; }</style>"), box, self.output]

    def on_value_change(self, change: dict):
        index = change["new"]
        device = self.output_devices[index]

        if self.callback != None:
            self.callback(device)

        with self.output:
            self.output.clear_output()
            print(device.as_output_str())  