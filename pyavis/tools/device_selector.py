from typing import Literal

from pyavis.shared.util import getInOutDevices
from pyavis.widgets import HBox, DropDown
from pyavis.backends.bases.widget_bases.widget import Widget
import pya

class DeviceSelector(Widget):
    def __init__(self, type: Literal["input", "output"]):
        self._server: pya.Aserver = None

        (input_list, output_list) = getInOutDevices()
        self._input_devices = input_list
        self._output_devices = output_list

        self._hb = HBox()
        if type == "input":
            self._dd = DropDown("Input", [device.as_input_str() for device in self._input_devices])
        elif type == "output":
            self._dd = DropDown("Input", [device.as_output_str() for device in self._output_devices])
        else:
            raise ValueError(f"'{type}' is not a valid selection type. Use either 'input' or 'output'.")
        
        self._hb.add_widget(self._dd)
        self._dd.add_on_selection_changed(lambda x: self.on_value_change(x))

    @property
    def server(self):
        return self._server

    def on_value_change(self, idx: int):
        if self.server:
            pya.Aserver.shutdown_default_server()
        self._server = pya.startup(device=self._output_devices[idx].index)

    def get_native_widget(self):
        return self._hb.get_native_widget()

    def show(self):
        self._hb.show()