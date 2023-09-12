from typing import Tuple

from pyavis.shared.util.subject import Subject
from .graphic_element import GraphicElement

class Spectrogram(GraphicElement):
    def __init__(self):
        GraphicElement.__init__(self)
        self.dataChanged = Subject()
        self.scaleChanged = Subject()
    
    def clear(self):
        pass

    def set_data(self, data):
        pass

    def set_scale(self, scale: Tuple[float, float]):
        pass

    def draw(self, draw_info):
        pass

