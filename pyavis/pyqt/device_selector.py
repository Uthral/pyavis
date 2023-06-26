from PySide2.QtWidgets import QWidget, QHBoxLayout, QComboBox
from pya import *
from typing import Callable

from pyavis.shared import getInOutDevices, DeviceInfo

class DeviceSelector(QWidget):
    def __init__(self, parent = None, callback: Callable[[DeviceInfo], None] = None):
        super(DeviceSelector, self).__init__(parent)

        (input_list, output_list) = getInOutDevices()
        self.input_devices = input_list
        self.output_devices = output_list
        self.callback = callback
        
        layout = QHBoxLayout()
        combo_box = QComboBox()
        layout.addWidget(combo_box)
        combo_box.addItems([ device.as_output_str() for device in output_list])

        combo_box.currentIndexChanged.connect(self.index_changed)
        
        self.setLayout(layout)
        self.setWindowTitle("Device Selector")
    
    def index_changed(self, index: int):
        device = self.output_devices[index]
        
        if self.callback != None:
            self.callback(device)  