import math
import numpy as np
from typing import List, Tuple
from ..util import Subject
from ..signal import Signal


class Track:
    def __init__(self, label: str, sampling_rate: int):
        self.label = label
        self.sampling_rate = sampling_rate
        self.signals: List[Tuple[int, Signal]] = []

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
    
    def __getitem__(self, index):
        """ 
        Accessing array elements through slicing.
            * slice, range and step slicing track[4:40:2]
                * Negative indexing and missing slice values use the tracks minimum length as basis.
                    * e.g. [-1:-500:-1] and [::1]
                * Use positive indexing if you want padding
            * Time slicing (unit in seconds) using dict track[{1:2.5}]
                * Indexing from 1s to 2.5s

        Parameters
        ----------
            index : slice or list or dict
                Slicing argument.

        Returns
        -------
        numpy.ndarray
            Array containing the signal values in the range. Values between signals are 0.
        """
        if isinstance(index, slice):
            idx = index
        elif isinstance(index, dict):
            for key, val in index.items():
                try:
                    start = int(key * self.sampling_rate)
                except TypeError: 
                    start = None
                try:
                    stop = int(val * self.sampling_rate)
                except TypeError:
                    stop = None
            idx = slice(start, stop, 1)
        else:
            raise TypeError("Not valid indexing")
        
        return self._get_signal_values(idx)
    
    def _get_signal_values(self, slice: slice):
        start, stop = slice.start, slice.stop

        # Calculate indicies for negative slice values
        new_start, new_stop, step = slice.indices(self.get_minimum_length())
        if start is None or start < 0:
            start = new_start
        if stop is None or stop < 0:
            stop = new_stop

        if start > stop and step > 0:
            return []
        elif start < stop and step < 0:
            return []
        elif start > stop and step < 0:
            return self._handle_indexing(stop, start, step)
        elif start < stop and step > 0:
            return self._handle_indexing(start, stop, step)
        else:
            return []
    
    def _handle_indexing(self, lower, higher, step):
        direction = "forward" if step > 0 else "backward"

        # Adjust size of array based on step size
        array = np.zeros(int(math.ceil(abs(higher - lower) / abs(step))))

        for pos, sig in self.signals:

            signal_start = pos
            signal_end = pos + len(sig.signal)

            if lower >= signal_end or higher <= signal_start:
                continue

            if direction == "forward":
                # Signal starts outside of range and ends in range
                if signal_start <= lower and signal_end <= higher:

                    # Divide stop index by step to allow both padding and step at the same time
                    array[0:int(math.ceil((signal_end - lower) / step))] = sig.signal[lower - signal_start::step]
                    
                # Signal starts in range and ends outside of range
                elif signal_start >= lower and signal_start < higher and signal_end > higher:
                    # TODO: Is divide here necessary
                    array[signal_start - lower:] = sig.signal[0:higher - signal_end:step]
                    
                # Range completly inside signal
                elif signal_start <= lower and signal_end >= higher:
                    array[:] = sig.signal[lower - signal_start:higher - signal_end:step]
                    
                # Signal lies completly in the range
                else:
                    pos_1 = signal_start - lower

                    # Step could lead to a situation where we do not start at the beginning of the array
                    # Account for that by calculation of the offset
                    padding = pos_1
                    remainder = padding % abs(step)
                    offset = step - remainder if not remainder == 0 else 0

                    array[math.ceil(pos_1 / step):] = sig.signal[offset::step]
                    
            elif direction == "backward":
                # Signal starts outside of range and ends in range
                if signal_start <= lower and signal_end <= higher:
                    # We can start from outside the array, we need to calculate the offset with which we enter the array
                    padding = higher - signal_end
                    remainder = padding % abs(step)
                    offset = step + remainder
                    
                    values = sig.signal[offset:lower - signal_start:step]
                    if not len(values) == 0:
                        array[-len(values):] = values
                    
                # Signal starts in range and ends outside of range
                elif signal_start >= lower and signal_start < higher and signal_end > higher:
                    # Since signal ends outsider of range, and were are going "backwards"
                    # -> Start at beginng of array
                    values = sig.signal[higher - signal_end:lower-signal_start:step]
                    array[:len(values)] = values
                    
                # Range completly inside signal
                elif signal_start <= lower and signal_end >= higher:
                    array[:] = sig.signal[higher - signal_end:lower - signal_start:step]
                    
                # Signal lies completly in the range
                else:
                    # We come from 'behind' -> possible offset necessary
                    padding = higher - signal_end # come from behind
                    remainder = padding % abs(step) # calc. what remains after enough steps
                    offset = step + remainder # padding is negative so -x + y => yields offset into array 

                    values = sig.signal[offset::step]
                    array[-len(values):] = values
            
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
    
    def get_minimum_length(self, type="samples") -> int | float:
        """
        Get the minimum length that the track occupies

        Parameter
        ---------
        type : str
            Return type (either "samples" or "seconds")

        Returns
        -------
        int | float
            Minimum length in samples or seconds
        """
        val = max(self.signals, key=lambda x: x[0])
        if type == "samples":
            return val[0] + len(val[1].signal)
        elif type == "seconds":
            return ( val[0] + len(val[1].signal) ) / self.sampling_rate
        else:
            raise ValueError("Not a valid argument")