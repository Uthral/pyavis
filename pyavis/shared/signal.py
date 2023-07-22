from pya import Asig

class AudioSignal:
    def __init__(self, asig: Asig, channel_index: int = None, channel_name: str = None):
        self.asig = asig
        self.channel_index = channel_index
        self.channel_name = channel_name

    def signal(self):
        if self.channel_index is None:
            return self.asig.sig
        else:
            return self.asig.sig[self.channel_index]
    
    def sampling_rate(self):
        return self.asig.sr