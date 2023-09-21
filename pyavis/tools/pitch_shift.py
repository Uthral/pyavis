from pyavis.backends.bases.widget_bases.widget import Widget
from pyavis.widgets import HBox, GraphicDisp, Button
from pyavis.graphics import Layout

import math
import pya
import numpy as np


class PitchShift(Widget):
    def __init__(self):
        self._signal = None
        self._sr = 44100
        self.signal_size = 8

        self._hb = HBox()
        self._disp = GraphicDisp()
        self._signal_disp = GraphicDisp()

        layout = Layout(1,1)
        signal_layout = Layout(1,1)

        self._track = layout.add_track("Shift", 0, 0)
        self._sig_track = signal_layout.add_track("Signal", 0, 0)

        self._disp.set_displayed_item(layout)
        self._signal_disp.set_displayed_item(signal_layout)

        self._hb.add_widget(self._disp)
        self._hb.add_widget(self._signal_disp)

        self._track.set_axis('left', spacing=None, disp_func=midi_conv)
        self._track.set_axis('bottom', spacing=None, disp_func=lambda value: f'{round(value / self._sr, 2)}')
        self._sig_track.set_axis('bottom', spacing=None, disp_func=lambda value: f'{round(value / self._sr, 2)}')

        self.selections = []
        self.sub_signals = []

        self._event2selection = {}
        self._selection2event = {}
        self._event2signal = {}
        self._selection2signal = {}

        self.mode = "shift_pitch"


    def set_signal(self, signal):
        if isinstance(signal, pya.Esig):
            self._signal = signal
            self._sr = self._signal.asig.sr
        elif isinstance(signal, pya.Asig):
            self._signal = pya.Esig(signal.mono())
            self._sr = self._signal.asig.sr
        else:
            raise TypeError("Signal must either be of type 'Esig' or 'Asig'.")

        if hasattr(self, "_gfx_spec"):
            self._track.remove(self._gfx_sig_1)
            self._sig_track.remove(self._gfx_sig_2)

            for s in self.sub_signals:
                self._track.remove(s)
            
            for s in self.selections:
                self._track.remove(s)

        self._gfx_sig_2 = self._sig_track.add_signal((0,0), "auto", y=self._signal.cache.asig.sig)

        for event in self._signal.cache.events:
            center = hz_2_midi(self._signal._avg_pitch(event))

            sig = self._track.add_signal((event.start, center), self.signal_size, self._signal.asig.sig[event.start:event.end])
            sig.set_style((255,0,0))

            selection = self._track.add_selection((event.start, center - self.signal_size / 2), event.end - event.start, self.signal_size)
            selection.set_style((150, 50, 150), (0, 255, 255))

            self.sub_signals.append(sig)
            self.selections.append(selection)

            self._event2selection[event] = selection
            self._selection2event[selection] = event
            self._event2signal[event] = sig
            self._selection2signal[selection] = sig


            self._handle_mode(selection)

        self.pitch_curve = None
        self._handle_pitch_curve()

    def _handle_mode_change(self, selection, previous_mode):
        if previous_mode == "shift_pitch":
                selection.draggable = False
                selection.clickable = False

                selection.onClick.clear()
                selection.onDraggingBegin.clear()
                selection.onDragging.clear()
                selection.onDraggingFinish.clear()

    def _handle_mode(self, selection):
        if self.mode == "shift_pitch":
            selection.draggable = True
            selection.onDragging.connect(lambda args: self._move_event(args[0], *args[1]))
            selection.onDraggingFinish.connect(lambda args: self._finish_move_event(args[0], *args[1]))

    def _move_event(self, selection, x, y):
        old_pos = selection.position
        selection.set_position(old_pos[0], y)

    def _finish_move_event(self, selection, x, y):
        event = self._selection2event[selection]
        event_id = self._signal.cache.events.index(event)

        # Adjust for size of signal / rectangle
        y += self.signal_size / 2

        self._signal.correct_event_pitch(event_id, np.array([(0,y),(1, y)]))
        
        # Change position of signal & adjust for signal size
        sig = self._event2signal[event]
        sig.set_position(x=sig.position[0], y=y)

        self._gfx_sig_2.set_data(y=self._signal.cache.asig.sig)

        self._handle_pitch_curve()

    def _handle_pitch_curve(self):
        if self.pitch_curve is not None:
            self._track.remove(self.pitch_curve)

        self.pitch_curve = self._track.add_signal(
            (0,0),
            "auto",
            y=hz_2_midi(self._signal.cache.pitch),
            x=self._signal.cache.frame_jump * np.linspace(0, len(self._signal.cache.pitch), num=len(self._signal.cache.pitch))
        )
        self.pitch_curve.set_style((0,0,0))

    def get_native_widget(self):
        return self._hb.get_native_widget()

    def show(self):
        self._hb.show()



def midi_conv(value) -> str:
    midi_value = int(value)
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',]
    octave = int(midi_value / 12 - 1)
    return f'{notes[midi_value % 12]}{octave}'

def midi_2_hz(value):
    power = (value - 69) / 12

    return 440 * np.power(2, power)

def hz_2_midi(value):
    return 12 * np.log2(value / 440) + 69