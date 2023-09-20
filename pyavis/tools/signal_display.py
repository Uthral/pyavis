from pyavis.backends.bases.widget_bases.widget import Widget
from pyavis.widgets import VBox, GraphicDisp, Button
from pyavis.graphics import Layout_v2

from pyavis.shared.multitrack import Track
from pyavis.shared import AudioSignal

import pya
import numpy as np


class SignalDisplay(Widget):
    def __init__(self):
        self._signal = None
        
        # Widgets
        self._vb = VBox()
        self._button = Button("Play")
        self._disp = GraphicDisp()
        
        # Graphic display items
        layout = Layout_v2(1,1)
        self._gfx_track = layout.add_track("Signal", 0, 0)
        self._gfx_track.add_line((0,0), 0).set_style((0,0,0))
        self._gfx_signal = None
        self._selection = None
        
        
        # Internal track
        self._track = Track("Signal", 44100)

        # Assign layout and widgets
        self._disp.set_displayed_item(layout)
        self._vb.add_widget(self._button)
        self._vb.add_widget(self._disp)

        # Add callback
        self._button.add_on_click(self._play)
    
    def set_signal(self, signal, channel=0):
        '''
        Set the signal that should be displayed. 
        If the signal has multiple channels, then display only one.
        
        Parameters
        ----------
        signal: Asig
            Audio signal to display
        channel: number | None
            Channel of the signal
        '''
        # Check for type
        if not isinstance(signal, pya.Asig):
            raise TypeError("'signal' has to be of type 'pya.Asig'")
        
        # If a signal has already been set, then clear display
        if self._signal is not None:
            self._gfx_track.remove(self._gfx_signal)
            self._gfx_track.remove(self._selection)
            self._gfx_signal = None
            self._selection = None

            self._track.remove_signal(self._sig)
            self._sig = None
        
        # Set signal and add graphical display
        self._signal = signal
        self._gfx_signal = self._gfx_track.add_signal((0,0), "auto", y=self._signal.sig)
        
        # Prepare internal track to allow better replay functionality
        self._track.sampling_rate = self._signal.sr
        self._sig = AudioSignal(signal, channel)
        self._track.try_add(0, self._sig)

    def set_selection(self, value):
        '''
        Set or unset selection.

        Parameters
        ----------
        value: None or (float, float)
            If None, removes active selection. If tuple, adds or replaces active selection.
        '''

        # Remove selection if one is active
        if value is None:
            if self._selection is not None:
                self._gfx_track.remove(self._selection)
            self._selection = None

        # Set / Replace selection
        elif isinstance(value, tuple) and len(value) == 2:
            if self._selection is not None:
                self._gfx_track.remove(self._selection)

            height = np.max(np.abs(self._signal.sig))
            self._selection = self._gfx_track.add_selection((value[0],-height), value[1], 2 * height)
            self._selection.set_style((255, 0, 0), (125, 0, 0))
            self._selection.add_handle("left", False)
            self._selection.add_handle("right", False)
        else:
            raise TypeError("Either None or (float, float)") 
        
    def _play(self):
        '''
        Play the displayed signal or selection of the signal.
        '''

        # If no selection has been set, then play entire signal
        if self._selection is None:
            val = self._track[:]
            pya.Asig(val, self._signal.sr).play()
        
        # If a selection is set, then only play selection
        else:
            x1 = int(self._selection.position[0])
            x2 = int(self._selection.size[0] + x1)

            val = self._track[x1:x2]
            pya.Asig(val, self._signal.sr).play()

    def get_native_widget(self):
        return self._vb.get_native_widget()

    def show(self):
        self._vb.show()

    