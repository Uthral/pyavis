from pya import Aserver, Asig, startup
from .util.subject import Subject
import time
import typing

class AudioPlayer:
    def __init__(self, sampling_rate: int = 44100, server: Aserver = None):
        self.sampling_rate = sampling_rate
        self.set_server(server)

        self.running = False
        self.paused = False
        
        self.start_time = None
        self.pause_time = None

        self.on_start = Subject()
        self.on_pause = Subject()
        self.on_stop = Subject()

    def set_audio(self, audio: Asig):
        # TODO: Replace with 'container' to allow selection and multiple at once
        self.audio = audio

    def start(self):
        if self.running:
            return
        elif self.paused:
            time = self.start_time - self.pause_time
            self.audio[time * self.sampling_rate:].play()
        else:
            self.start_time = time.time()
            self.audio.play()
            self.on_start.emit(self)

    def pause(self):
        if self.running:
            self.paused = True
            self.pause_time = time.time()
            self.server.stop()
            self.on_pause.emit(self)
            

    def stop(self):
        if self.running or self.paused:
            self.server.stop()
            
            self.running: bool = False
            self.paused: bool = False
            self.start_time: float | None = None
            self.pause_time: float | None = None

            self.on_stop.emit(self)

    def get_time(self) -> typing.Optional[float]:
        if self.running:
            return time.time() - self.start_time
        elif self.paused:
            return self.pause_time - self.start_time
        else:
            return None

    def set_server(self, server: Aserver = None):
        if server == None:
            self.server = startup(sampling_rate=self.sampling_rate)
        else:
            self.server = server