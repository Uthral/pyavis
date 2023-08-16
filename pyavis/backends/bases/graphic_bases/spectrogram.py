from typing import Tuple
from .graphic_element import GraphicElement

class Spectrogram(GraphicElement):
    def __init__(self):
        GraphicElement.__init__(self)
    
    def set_size(self, size: Tuple[float, float]):
        pass