import numpy as np
from typing import List, Tuple
from ..util import Subject
from ..signal import Signal


class Track:
    def __init__(self):
        self.signals: List[Tuple[int, Signal]] = []
        self._selection_start = None
        self._selection_end = None

        self.onSignalAdded = Subject()
        self.onSignalMoved = Subject()
        self.onSignalRemoved = Subject()

        self.onSelectionAdded = Subject()
        self.onSelectionUpdated = Subject()
        self.onSelectionRemoved = Subject()

    def get_section(self, start: int, end: int) -> np.ndarray:
        """
        Return the values in the range.

        Parameters
        ----------
        start : int
            Start of the range
        end : int
            End of the range

        Returns
        -------
        numpy.ndarray
            Array containing the signal values in the range. Values between signals are 0.
        """
        array = np.zeros((end-start))

        for pos, signal in self.signals:
            signal_start, signal_end = pos, pos + len(signal.signal)

            # Signal starts outside of range
            if signal_start < start and signal_end < end:
                array[0:signal_end - start] = signal.signal[start - signal_start:]
            # Signal ends outside of range
            elif signal_start > start and signal_end > end:
                array[signal_start - start:-1] = signal.signal[0:end - signal_end]
            # Signal lies completly in the range
            else:
                pos_1 = signal_start - start
                pos_2 = pos_1 + len(signal.signal)
                array[pos_1: pos_2] = signal.signal[:]
            
        return array
    
    def set_selection(self, start: int, end: int):
        if self._selection_start is None and self._selection_end is None:
            self._selection_start = start
            self._selection_end = end
            self.onSelectionAdded.emit(self, start, end)
        else:
            self._selection_start = start
            self._selection_end = end
            self.onSelectionUpdated.emit(self, start, end)

    def remove_selection(self):
        if self._selection_end is not None and self._selection_end is not None:
            self._selection_start = None
            self._selection_end = None
            self.onSelectionRemoved.emit(self)
    
    def get_selection(self) -> np.ndarray | None:
        if self._selection_start is None or self._selection_end is None:
            return None
        else:
            return self.get_section(self._selection_start, self._selection_end)
    
    def get_index(self, pos: int, signal: Signal) -> int:
        """
        Get index of the signal

        Parameters
        ----------
        pos : int
            Position of the signal
        signal : Signal
            The signal

        Returns
        -------
        int
            Index of the signal
        """
        return self.signals.index((pos, signal))
    
    def get_signal_at_position(self, pos: int) -> Tuple[int,Signal] | None:
        """
        Get signal at the position

        Parameters
        ----------
        pos : int
            Position of the signal

        Returns
        -------
        (int, Signal) | None
            Returns a signal, if there is one at the position
        """
        value = next(filter(lambda item: pos >= item[0] and pos < item[0] + len(item[1].signal), self.signals), None)
        return value


    def try_add(self, pos: int, signal: Signal) -> bool:
        '''
        Try adding the signal at the positioin position to the track.

        Parameters
        ----------
        pos : int
            Positon of the new signal
        signal : Signal
            Signal to ad

        Returns
        -------
        '''
        if self.can_add_at(pos, signal):
            self.signals.append((pos, signal))
            self.onSignalAdded.emit(self, pos, signal)
            return True
        else:
            return False

    def can_add_at(self, pos: int, signal: Signal) -> bool:
        """
        Check if a signal can be added at the position

        Parameters
        ----------
        pos : int
            Positon of the new signal in the track
        signal : Signal
            Signal to add
        """
        start, end = pos, pos + len(signal.signal)
        for iter_idx, (iter_pos, iter_signal) in enumerate(self.signals):
            iter_start, iter_end = iter_pos, iter_pos + len(iter_signal.signal)
            if start > iter_start and start < iter_end:
                return False
            if end > iter_start and end < iter_end:
                return False
        return True
    
    def remove(self, pos: int, signal: Signal):
        '''
        Remove the signal at the position.

        Parameters
        ----------
        pos: int
            Position of the signal
        signal: Signal
            Signal to delete
        '''
        self.signals.remove((pos, signal))
        self.onSignalRemoved(self, pos, signal)

    def try_move(self, pos: int, idx: int) -> bool:
        '''
        Try moving the signal to the new position.

        Parameters
        ----------
        pos : int
            New positon of the signal in the track
        idx : int
            Index of the signal

        Returns
        -------

        '''
        if self.can_move_to(pos, idx):
            value = list(self.signals[idx]) 
            value[0] = pos
            self.signals[idx] = tuple(value)
            self.onSignalMoved.emit(self, pos, value[1])
            return True
        else:
            return False

    def can_move_to(self, pos: int, idx: int) -> bool:
        '''
        Check if the signal can be moved to the position.

        Parameters
        ----------
        pos : int
            New positon of the signal in the track
        idx : int
            Index of the signal

        Returns
        -------

        '''
        (_, signal) = self.signals[idx]
        
        start, end = pos, pos + len(signal.signal)
        for iter_idx, (iter_pos, iter_signal) in enumerate(self.signals):
            # Ignore current signal, since it will be moved.
            if iter_idx == idx:
                continue
            iter_start, iter_end = iter_pos, iter_pos + len(iter_signal.signal)
            if start > iter_start and start < iter_end:
                return False
            if end > iter_start and end < iter_end:
                return False
        return True
        