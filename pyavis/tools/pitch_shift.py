from pyavis.backends.bases.widget_bases.widget import Widget
from pyavis.widgets import VBox, GraphicDisp, Button, Toolbar
from pyavis.graphics import Layout

import pya
import numpy as np


class PitchShift:
    def __init__(self):
        self.internal_signal = None
        self.signal_size = 2

        self._prepare_pitch_shift()
        self._prepare_signal()

        self.handle_toolbar_mode()

        self.selections = []
        self.sub_signals = []

        self._event2selection = {}
        self._selection2event = {}
        self._event2signal = {}
        self._selection2signal = {}

        self.mode = "move"

    def _prepare_pitch_shift(self):
        # Create necessary widgets for displaying and shifting signal
        self.pitch_shift_toolbar = Toolbar(["Move", "Edit"], ["move", "edit"])
        self.pitch_shift_display = GraphicDisp()

        # Create layout and add view
        layout = Layout(1,1)
        self.pitch_shift_view = layout.add_track("Pitch shift", 0, 0)
        self.pitch_shift_display.set_displayed_item(layout)

        self.pitch_shift_view.set_axis(
            'left',
            spacing=None,
            disp_func=midi_conv
        )

        self.pitch_shift_view.set_axis(
            'bottom',
            spacing=None,
            disp_func=lambda value: f'{round(value / self.internal_signal.asig.sr, 2)}'
        )

        # Combine widgets in box
        vertical_box = VBox()
        vertical_box.add_widget(self.pitch_shift_toolbar)
        vertical_box.add_widget(self.pitch_shift_display)

        self.pitch_shift_widget = vertical_box
        

    def _prepare_signal(self):
        # Create necessary widgets for displaying and playing signal
        self.signal_play_button = Button("Play")
        self.signal_display = GraphicDisp()

        # Create layout and add view
        layout = Layout(1,1)
        self.signal_view = layout.add_track("Signal", 0, 0)
        self.signal_display.set_displayed_item(layout)

        self.signal_view.set_axis('bottom', spacing=None, disp_func=lambda value: f'{round(value / self.internal_signal.asig.sr, 2)}')

        # Combine widgets in box
        vertical_box = VBox()
        vertical_box.add_widget(self.signal_play_button)
        vertical_box.add_widget(self.signal_display)

        self.signal_play_button.add_on_click(self.play_audio)

        self.signal_widget = vertical_box

    def set_signal(self, signal):
        if self.internal_signal is not None:
            for x in self.sub_signals:
                self.pitch_shift_view.remove(x)
            for x in self.selections:
                self.pitch_shift_view.remove(x)
            self.pitch_shift_view.remove(self.pitch_curve)

            self.signal_view.remove(self.signal_graphic)

        if isinstance(signal, pya.Esig):
            self.internal_signal = signal
        elif isinstance(signal, pya.Asig):
            self.internal_signal = pya.Esig(signal.mono())
        else:
            raise TypeError("Signal must either be of type 'Esig' or 'Asig'.")
        
        self.signal_graphic = self.signal_view.add_signal((0,0), 1.0, y=self.internal_signal.cache.asig.sig)

        for event in self.internal_signal.cache.events:
            center = hz_2_midi(self.internal_signal._avg_pitch(event))
            sig = self.pitch_shift_view.add_signal(
                (event.start, center),
                self.signal_size,
                self.internal_signal.asig.sig[event.start:event.end]
            )
            sig.set_style((255,0,0))

            selection = self.pitch_shift_view.add_selection(
                (event.start, center - self.signal_size / 2),
                event.end - event.start,
                self.signal_size
            )

            selection.set_style((150, 50, 150), (0, 255, 255))
            selection.onDragging.connect(lambda selection, pos: self.move_selection_event(selection, *pos))
            selection.onDraggingFinish.connect(lambda selection, pos: self.finish_move_selection_event(selection, *pos))

            self.sub_signals.append(sig)
            self.selections.append(selection)

            self._event2selection[event] = selection
            self._selection2event[selection] = event
            self._event2signal[event] = sig
            self._selection2signal[selection] = sig

        
        self.pitch_curve = None
        self.handle_pitch_curve()
        self.handle_mode_change()

    def handle_pitch_curve(self):
        if self.pitch_curve is not None:
            self.pitch_shift_view.remove(self.pitch_curve)

        self.pitch_curve = self.pitch_shift_view.add_signal(
            (0,0),
            1.0,
            y=hz_2_midi(self.internal_signal.cache.pitch),
            x=self.internal_signal.cache.frame_jump * np.linspace(0, len(self.internal_signal.cache.pitch), num=len(self.internal_signal.cache.pitch))
        )
        self.pitch_curve.set_style((0,0,0))

    def handle_toolbar_mode(self):
        self.pitch_shift_toolbar.add_on_active_changed(self.handle_mode_change)

    def handle_mode_change(self, _ = None):
        if self.pitch_shift_toolbar.get_active_value() == "move":
            for x in self.selections:
                x.draggable = False
                x.clickable = False
        elif self.pitch_shift_toolbar.get_active_value() == "edit":
            for x in self.selections:
                x.draggable = True
                x.clickable = True

    def move_selection_event(self, selection, x, y):
        selection.set_position(selection.position[0], y)

    def finish_move_selection_event(self, selection, x, y):
        event = self._selection2event[selection]
        event_id = self.internal_signal.cache.events.index(event)

        # Change position of signal & adjust for signal size
        sig = self._event2signal[event]
        sig_position = sig.position
        
        y += self.signal_size / 2

        self.internal_signal.change_event_pitch(event_id, y - sig_position[1])
        sig.set_position(x=sig.position[0], y=y)

        self.signal_graphic.set_data(y=self.internal_signal.cache.asig.sig)
        self.handle_pitch_curve()

    def play_audio(self, args):
        # Play the asig
        self.internal_signal.cache.asig.play()

    def show(self):
        self.signal_widget.show()
        self.pitch_shift_widget.show()


def midi_conv(value) -> str:
    midi_value = int(value)
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',]
    octave = int(midi_value / 12 - 1)
    return f'{notes[midi_value % 12]}{octave}'

def midi_2_hz(value):
    power = (value - 69) / 12

    return 440 * np.power(2, power)

def hz_2_midi(value):
    result = 12 * np.log2(value / 440, where=value > 0) + 69
    return np.clip(result, 0,130)