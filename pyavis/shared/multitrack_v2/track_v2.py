import math
import numpy as np

class Track:
    """Represents one audio channel"""
    def __init__(self, name: str, sampling_rate: int, signal):
        self.name = name
        self.sampling_rate = sampling_rate

        self.signal: np.ndarray = signal
    
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
        new_start, new_stop, step = slice.indices(len(self.signal))
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

        signal_start = 0
        signal_end = len(self.signal)

        # Adjust size of array based on step size
        array = np.zeros(int(math.ceil(abs(higher - lower) / abs(step))))

        if lower > signal_end:
            return array

        if direction == "forward":
            # Signal starts outside of range
            if signal_start <= lower and signal_end <= higher:
                # Divide stop index by step to allow both padding and step at the same time
                array[0:int(math.ceil((signal_end - lower) / step))] = self.signal[lower - signal_start::step]
                
            # Signal ends outside of range
            elif signal_start >= lower and signal_end >= higher:
                # TODO: Is divide here necessary
                array[signal_start - lower:] = self.signal[0:higher - signal_end:step]
                
            # Range completly inside signal
            elif signal_start <= lower and signal_end >= higher:
                array[:] = self.signal[lower - signal_start:higher - signal_end:step]
                
            # Signal lies completly in the range
            else:
                pos_1 = signal_start - lower
                pos_2 = pos_1 + len(self.signal)
                # TODO: Is divide here necessary
                array[pos_1: pos_2] = self.signal[::step] 
                
        elif direction == "backward":
            # Signal starts outside of range
            if signal_start <= lower and signal_end <= higher:
                # We can start from outside the array, we need to calculate the offset with which we enter the array
                padding = higher - signal_end
                remainder = padding % abs(step)
                offset = step + remainder
                
                values = self.signal[offset:lower - signal_start:step]
                if not len(values) == 0:
                    array[-len(values):] = values
                
            # Signal ends outside of range
            elif signal_start >= lower and signal_end >= higher:
                # TODO: Is divide here necessary
                array[signal_start - lower:] = self.signal[higher - signal_end:0:step]
                
            # Range completly inside signal
            elif signal_start <= lower and signal_end >= higher:
                array[:] = self.signal[higher - signal_end:lower - signal_start:step]
                
            # Signal lies completly in the range
            else:
                pos_1 = signal_start - lower
                pos_2 = pos_1 + len(self.signal)
                # TODO: Is divide here necessary
                array[pos_1: pos_2] = self.signal[::step]
        
        return array


