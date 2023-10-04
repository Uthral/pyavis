from typing import Tuple
from pyavis.backends.bases.graphic_bases import RectSelection

import warnings

class RectSelectionIPY(RectSelection):
    def __init__(
            self,
            position: Tuple[float, float],
            size: Tuple[float, float]
    ):
        RectSelection.__init__(self, position, size)
        warnings.warn("'RectSelection' not implemented for ipywidget backend.")
