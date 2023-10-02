from pya import Asig

class AudioSignal:
    def __init__(self, asig: Asig, channel_index: int = None, channel_name: str = None):
        self.asig = asig
        self.channel_index = channel_index
        self.channel_name = channel_name

    def signal(self):
        if self.channel_index is not None and self.asig.channels > 1:
            return self.asig.sig[:, self.channel_index]
        elif self.channel_name is not None:
            return self.asig.sig[self.channel_name]
        else:
            return self.asig.sig

    def sampling_rate(self):
        return self.asig.sr