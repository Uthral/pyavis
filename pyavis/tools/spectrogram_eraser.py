
import pya, numpy
from pyavis.widgets import GraphicDisp, Toolbar, Button, VBox
from pyavis.graphics import Layout
from pyavis.shared.util.util import spec_to_asig

import numpy as np

class SpectrogramEraser:
    def __init__(self):
        # Built the two widgets
        self._build_spectrogram()
        self._build_signal()

        self.internal_signal = None
        self.display_signal = None
        

    def _build_spectrogram(self):
        # Create necessary widgets for displaying and editing spectrogram
        self.spectrogram_toolbar = Toolbar(["Move", "Edit"], ["move", "edit"])
        self.spectrogram_display = GraphicDisp()

        # Create layout and add view
        layout = Layout(1,1)
        self.spectrogram_view = layout.add_track("Spectrogram", 0, 0)
        self.spectrogram_display.set_displayed_item(self.spectrogram_view)

        # Combine widgets in box
        vertical_box = VBox()
        vertical_box.add_widget(self.spectrogram_toolbar)
        vertical_box.add_widget(self.spectrogram_display)

        self.spectrogram = vertical_box


    def _build_signal(self):
        # Create necessary widgets for displaying and playing signal
        self.signal_play_button = Button("Play")
        self.signal_display = GraphicDisp()

        # Create layout and add view
        layout = Layout(1,1)
        self.signal_view = layout.add_track("Signal", 0, 0)
        self.signal_display.set_displayed_item(self.signal_view)

        self.signal_view.set_axis('bottom', spacing=None, disp_func=lambda value: f'{round(value / self.signal.sr, 2)}')

        # Combine widgets in box
        vertical_box = VBox()
        vertical_box.add_widget(self.signal_play_button)
        vertical_box.add_widget(self.signal_display)

        self.signal = vertical_box

    def set_singal(self, signal):
        if self.internal_signal is not None:
            self.signal_view.remove(self.signal_graphic)
            self.spectrogram_view.remove(self.spectrogram_graphic)
        
        self.internal_signal = signal
        self.display_signal = signal

        self.signal_graphic = self.signal_view.add_signal(y=self.display_signal.sig)
        self.spectrogram_graphic = self.spectrogram_view.add_spectrogram(
            data=self.internal_signal,
            disp_func=lambda x: pya.ampdb(numpy.abs(x))
        )

        self.handle_callbacks()
        self.handle_toolbar_mode()
        self.mode_change()

    def handle_toolbar_mode(self):
        self.spectrogram_toolbar.add_on_active_changed(self.mode_change)

    def handle_callbacks(self):
        # Add all necessary callbacks to the graphics
        self.spectrogram_graphic.onDragging.connect(self.draw_on_spectrogram)
        self.spectrogram_graphic.onDraggingFinish.connect(self.update_signal)

        self.signal_play_button.add_on_click(self.play_audio)

    def set_eraser(self, frequency_slices, time_slices):
        # Set the eraser size/values and the center
        self.eraser = -140 * np.ones((time_slices, frequency_slices))
        self.center = (int(time_slices / 2), int(frequency_slices / 2))

    def mode_change(self, _ = None):
        if self.spectrogram_toolbar.get_active_value() == "move":
            self.spectrogram_graphic.draggable = False
            self.spectrogram_graphic.clickable = False
        elif self.spectrogram_toolbar.get_active_value() == "edit":
            self.spectrogram_graphic.draggable = True
            self.spectrogram_graphic.clickable = True

    def draw_on_spectrogram(self, element, pos):
        # Draw on the spectrogram image
        freq, time = pos[1], pos[0]
        self.spectrogram_graphic.set_brush(brush_data = self.eraser, brush_center = self.center)
        self.spectrogram_graphic.draw(freq, time)
        self.spectrogram_graphic.clear_brush()

    def update_signal(self, element, pos):
        # Convert spectrogram back to audio signal using the original phase
        self.signal_view.remove(self.signal_graphic)
        self.display_signal = spec_to_asig(self.spectrogram_graphic, inverted_display_func=pya.dbamp, with_original_phase=True)
        self.signal_graphic = self.signal_view.add_signal(y=self.display_signal.sig)

    def play_audio(self, args):
        # Play the asig
        self.display_signal.play()

    def show(self):
        # Show both widgets
        self.spectrogram.show()
        self.signal.show()

