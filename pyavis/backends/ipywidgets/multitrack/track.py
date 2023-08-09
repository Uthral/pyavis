from matplotlib.axes import Axes
from overrides import override
from pyavis.base_classes import BaseTrack
from pyavis.shared.multitrack.track import Track

class M_TrackIPY(type(BaseTrack), type(Axes)): pass
class TrackIPY(BaseTrack, Axes, metaclass=M_TrackIPY):
    def set_data(self, label: str, sampling_rate: int):
        self.label = label
        self.sampling_rate = sampling_rate
        self.track = Track(label, sampling_rate)
        self.set_ylabel(self.label)

    @override
    def add_signal(self, position: int, signal, **kwargs):
        success = self.track.try_add(position, signal)
        if not success:
            raise ValueError("Could not add signal")

        for pos, signal in self.track.signals:
            self.plot(range(pos, pos + len(signal.signal())), signal.signal())

    @override
    def remove_signal(self, signal):
        (position, signal) = self.track.get_signal(signal)
        success = self.track.remove(position, signal)
        if not success:
            raise ValueError("Could not remove signal")
        
        for pos, signal in self.track.signals:
            self.plot(range(pos, pos + len(signal.signal())), signal.signal())

    @override
    def remove_at_position(self, position: int):
        result = self.track.get_signal_at_position(position)
        if result is None:
            raise ValueError("Could not remove signal")
        
        (position, signal) = result
        self.track.remove(position, signal)

        for pos, signal in self.track.signals:
            self.plot(range(pos, pos + len(signal.signal)), signal.signal())


    @override
    def __getitem__(self, index):
        return self.track[index]

import matplotlib.projections as proj
proj.register_projection(TrackIPY)