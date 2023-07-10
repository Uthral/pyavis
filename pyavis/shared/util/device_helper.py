from pya import helper
from typing import Tuple, List


class DeviceInfo:
    def __init__(self, index, name, sr, nr_input, nr_output):
        self.index = index
        self.name = name
        self.sampling_rate = sr
        self.nr_input = nr_input
        self.nr_output = nr_output

    def as_output_str(self) -> str:
        return f"{self.index}: {self.name:50s} ({self.nr_output} chns @ {self.sampling_rate:5.0f} Hz)"

    def as_input_str(self) -> str:
        return f"{self.index}: {self.name:50s} ({self.nr_input} chns @ {self.sampling_rate:5.0f} Hz)"


def getInOutDevices() -> Tuple[List[DeviceInfo], List[DeviceInfo]]:
    input_list, output_list = [], []

    for device in helper.device_info():
        i = device['index']
        name = device['name']
        sr = device['defaultSampleRate']
        nr_inp = device['maxInputChannels']
        nr_out = device['maxOutputChannels']

        dev = DeviceInfo(i, name, sr, nr_inp, nr_out)

        if nr_inp > 0: 
            input_list.append(dev)
        if nr_out > 0:
            output_list.append(dev)

    return (input_list, output_list)