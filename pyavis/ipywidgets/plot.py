from matplotlib.pyplot import figure, show
from matplotlib.widgets import Button, Slider
from matplotlib.figure import Figure

import numpy as np
import pya 

class AudioPlotFigure(Figure):
    """A figure for displaying audio data"""
    
    def __init__(self, *args, audio: pya.Asig, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio = audio

        padding = 0.1
        yMin, yMax = np.min(self.audio.sig), np.max(self.audio.sig)
        xMin, xMax = 0.1, audio.samples

        self.ax = self.add_subplot(111, xlim=(0, audio.sr * xMin), ylim=(yMin - padding,yMax + padding))
        self.subplots_adjust(bottom=0.3)
        self.setAxisFormatter("time")

        # TODO: Maybe move interactivity out of here and allow usage of other
        #       UI methods
        y_ax = self.add_axes([0.25, 0.15, 0.65, 0.03])
        self.y_slider = Slider(
            ax=y_ax,
            label='Range [s]',
            valmin=xMin,
            valmax=xMax / audio.sr,
            valinit=xMin
        )

        x_ax = self.add_axes([0.25, 0.10, 0.65, 0.03])
        self.x_slider = Slider(
            ax=x_ax,
            label='Position [%]',
            valmin=0.0,
            valmax=1.0,
            valinit=0.0
        )

        play_ax = self.add_axes([0.8, 0.025, 0.1, 0.04])
        self.play_button = Button(play_ax, 'Play', hovercolor='0.975')
        stop_ax = self.add_axes([0.65, 0.025, 0.1, 0.04])
        self.stop_button = Button(stop_ax, 'Stop', hovercolor='0.975')

        self.play_button.on_clicked(self.onPlayClick)
        self.stop_button.on_clicked(self.onStopClick)

        self.x_slider.on_changed(self.onXSliderChange)
        self.y_slider.on_changed(self.onYSliderChange)

        self.ax.plot(audio.sig)


    # TODO: Play / Stop functionality present in both: extract
    # TODO: Add Pause functionality
    def onPlayClick(self, event):
        self.audio.play()

    def onStopClick(self, event):
        server = pya.Aserver.default
        server.stop()

    def onYSliderChange(self, event):
        # Get center position in samples
        center_pos = self.x_slider.val * self.audio.samples
        # Get view range in samples
        view_range = event * self.audio.sr

        view_start = center_pos - view_range / 2
        view_end = center_pos + view_range / 2

        if view_start <= 0:
            view_start = 0
            view_end = view_range
        elif view_end >= self.audio.samples:
            view_start = self.audio.samples - view_range
            view_end = self.audio.samples

        self.ax.set_xlim((view_start, view_end))
        self.ax.figure.canvas.draw()

    def onXSliderChange(self, event):
        # Get center position in samples
        center_pos = event * self.audio.samples
        # Get view range in samples
        view_range = self.y_slider.val * self.audio.sr

        view_start = center_pos - view_range / 2
        view_end = center_pos + view_range / 2

        if view_start <= 0:
            view_start = 0
            view_end = view_range
        elif view_end >= self.audio.samples:
            view_start = self.audio.samples - view_range
            view_end = self.audio.samples

        self.ax.set_xlim((view_start, view_end))
        self.ax.figure.canvas.draw()

    def setAxisFormatter(self, axis_type="sample"):
        if axis_type == "sample":
            self.ax.xaxis.set_major_formatter(lambda x, pos: sampleAxisFormatter(x))
        elif axis_type == "time":
            self.ax.xaxis.set_major_formatter(lambda x, pos: timeAxisFormatter(x, self.audio.sr))


def timeAxisFormatter(x, sampling_rate):
    return "{:.2f}".format(x / sampling_rate)


def sampleAxisFormatter(x):
    return "{}".format(x)

