from matplotlib import gridspec
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import List

from overrides import override
from ..multitrack.selection import SelectionIPY
from ..multitrack.track import TrackIPY

from pyavis.base_classes import BaseSelection, BaseMultiTrack, BaseTrack

class MultiTrackIPY(BaseMultiTrack):
    def __init__(self, *args, **kwargs):
        self.figure = plt.figure(*args, **kwargs)
        self.figure.subplots_adjust(hspace=0)

        self.row = 0

        self.selections: List[BaseSelection] = []
        self.tracks: List[TrackIPY] = []
        
        self.selecting = True
            

    def get_native_widget(self):
        return self.figure.canvas
    
    @override
    def add_selection(self, indices, start, end) -> BaseSelection:
        selection = SelectionIPY(indices, start, end, fig=self.figure)
        self.selections.append(selection)
        return selection
    
    @override
    def remove_selection(self, selection: BaseSelection):
        self.selections.remove(selection)

    @override
    def add_track(self, label: str, sampling_rate: int, **kwargs) -> BaseTrack:
        self.row += 1
        gs = gridspec.GridSpec(self.row, 1)

        for i, ax in enumerate(self.figure.axes):
            ax.set_position(gs[i].get_position(self.figure))
            ax.set_subplotspec(gs[i])
            ax.xaxis.set_tick_params(labelbottom=False)

        if self.row != 1:
            new_ax = self.figure.add_subplot(gs[self.row-1], axes_class=TrackIPY, sharex=self.figure.axes[0])
        else:
            new_ax = self.figure.add_subplot(gs[self.row-1], axes_class=TrackIPY)
        
        new_ax.set_data(label, sampling_rate)
        self.figure.canvas.draw_idle()
        
        self.tracks.append(new_ax)

        return new_ax
        

    @override
    def remove_track(self, identifier: int | str | BaseTrack):
        if isinstance(identifier, BaseTrack):
            idx = self.tracks.index(identifier)
        elif isinstance(identifier, str):
            track = next(filter(lambda item: item.label == identifier, self.tracks), None)
            idx = self.tracks.index(track)
        elif isinstance(identifier, int):
            idx = identifier
        else:
            raise TypeError("Not a valid type.")
        
        print(idx)

        to_remove = self.tracks.pop(idx)
        self.figure.delaxes(to_remove)

        self.row -= 1
        gs = gridspec.GridSpec(self.row, 1)

        for i, ax in enumerate(self.figure.axes):
            ax.set_position(gs[i].get_position(self.figure))
            ax.set_subplotspec(gs[i])
            ax.xaxis.set_tick_params(labelbottom=False)

        self.figure.axes[-1].xaxis.set_tick_params(labelbottom=True)

        self.figure.canvas.draw_idle() 

    @override
    def update_track_height(self, track_height: int):
        pass

    @override
    def __getitem__(self, index):
        pass



