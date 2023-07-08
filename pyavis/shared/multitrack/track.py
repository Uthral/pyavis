import numpy as np
from typing import List, Tuple
from ..signal import Signal

class Track:
    def __init__(self):
        self.signals: List[Tuple[int, Signal]] = []

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
        