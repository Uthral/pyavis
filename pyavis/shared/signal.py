from typing import Tuple

class Signal:
    def __init__(self, signal):
        self.signal = signal

def split_sample(sample: Signal, at: int) -> Tuple[Signal, Signal]:
    l = Signal(sample.signal[:at])
    r = Signal(sample.signal[at:])
    return (l, r)