from pyavis.pyqt import DeviceSelector
from pyavis.shared.device_util import DeviceInfo
from pyqtgraph.Qt import QtWidgets
import pya
from pya import Aserver, startup
import numpy as np

signal_array = np.sin(2 * np.pi * 200 * np.linspace(0, 1, 44100))
atone = pya.Asig(signal_array, sr=44100, label='1s sine tone', cn=['left'])

s = None
def on_value_change(device_info: DeviceInfo):
    global s, atone
    if s:
        Aserver.shutdown_default_server()
    device_id = device_info.index
    s = startup(device=device_id)
    atone.play()

app = QtWidgets.QApplication()
selector = DeviceSelector(callback=on_value_change)
selector.show()
app.exec_()