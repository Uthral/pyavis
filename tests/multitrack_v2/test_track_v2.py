import numpy as np
from unittest import TestCase
from pyavis.shared.multitrack_v2 import Track

class TestTrackV2(TestCase):
    def setUp(self) -> None:
        self.sr = 44100
        self.signal = np.sin(2 * np.pi * 50 * np.linspace(0, 1, self.sr * 2))
        self.track = Track("Test", self.sr, self.signal)

    def test_invalid_indexing(self):
        with self.assertRaises(TypeError):
            self.track[1]
        
        with self.assertRaises(TypeError):
            self.track["a"]
        
        with self.assertRaises(TypeError):
            self.track[[1,2,3]]
    
    def test_positive_indexing(self):
        np.testing.assert_array_equal(self.track[0:100], self.signal[0:100])
        np.testing.assert_array_equal(self.track[100:5000], self.signal[100:5000])
        np.testing.assert_array_equal(self.track[20000:], self.signal[20000:])
        np.testing.assert_array_equal(self.track[:], self.signal[:])

        np.testing.assert_array_equal(self.track[4000:2000:-1],self.signal[4000:2000:-1])

    def test_negative_indexing(self):
        np.testing.assert_array_equal(self.track[0:-100], self.signal[0:-100])

        np.testing.assert_array_equal(self.track[-100:0:-1], self.signal[-100:0:-1])
    
    def test_positive_indexing_with_step(self):
        for i in range(1, 50, 1):
            np.testing.assert_array_equal(self.track[0:100:i], self.signal[0:100:i])
            np.testing.assert_array_equal(self.track[100:5000:i], self.signal[100:5000:i])
            np.testing.assert_array_equal(self.track[20000:-1:i], self.signal[20000:-1:i])

        for i in range(-1, -50, -1):
            np.testing.assert_array_equal(self.track[100:0:i], self.signal[100:0:i])
            np.testing.assert_array_equal(self.track[5000:100:i], self.signal[5000:100:i])
            np.testing.assert_array_equal(self.track[-1:20000:i], self.signal[-1:20000:i])

    def test_positive_indexing_with_padding(self):
        conc = np.zeros((self.sr))
        def concat(arr):
            return np.concatenate((arr, conc))

        np.testing.assert_array_equal(self.track[:self.sr * 3], concat(self.signal)[:self.sr * 3])
        np.testing.assert_array_equal(self.track[41000:self.sr * 3], concat(self.signal)[41000:self.sr * 3])
        np.testing.assert_array_equal(self.track[self.sr * 2:self.sr * 3], concat(self.signal)[self.sr * 2:self.sr * 3])
        np.testing.assert_array_equal(self.track[len(self.signal) + 1:self.sr * 3], concat(self.signal)[len(self.signal) + 1:self.sr * 3])

        idx = self.sr * 2
        np.testing.assert_array_equal(self.track[idx-25:idx+25], concat(self.signal)[idx-25:idx+25])

        np.testing.assert_array_equal(self.track[idx+5:idx-5:-1], concat(self.signal)[idx+5:idx-5:-1])
        np.testing.assert_array_equal(self.track[idx+500:idx-500:-1], concat(self.signal)[idx+500:idx-500:-1])
        np.testing.assert_array_equal(self.track[idx+500:idx+250:-1], concat(self.signal)[idx+500:idx+250:-1])
    
    def test_positive_indexing_with_padding_and_step(self):
        conc = np.zeros((self.sr))
        def concat(arr):
            return np.concatenate((arr, conc))
        
        idx = self.sr * 2
        np.testing.assert_array_equal(self.track[idx-25:idx+25:2], concat(self.signal)[idx-25:idx+25:2])
        np.testing.assert_array_equal(self.track[:idx+500:4], concat(self.signal)[:idx+500:4])
        np.testing.assert_array_equal(self.track[idx+250:idx+500:4], concat(self.signal)[idx+250:idx+500:4])
        for i in range(-1, -20, -1):
            np.testing.assert_array_equal(self.track[idx+3:idx-3:i], concat(self.signal)[idx+3:idx-3:i])
            np.testing.assert_array_equal(self.track[idx+100:idx-100:i], concat(self.signal)[idx+100:idx-100:i])
            np.testing.assert_array_equal(self.track[idx+500:idx-500:i], concat(self.signal)[idx+500:idx-500:i])
        
    def test_time_indexing(self):
        np.testing.assert_array_equal(self.track[{1:2}], self.signal[self.sr:self.sr*2])

    def test_time_indexing_with_padding_and_step(self):
        conc = np.zeros((self.sr))
        def concat(arr):
            return np.concatenate((arr, conc))
        
        np.testing.assert_array_equal(self.track[{1:3}], concat(self.signal)[self.sr:self.sr*3])
        np.testing.assert_array_equal(self.track[{1.5:3}], concat(self.signal)[int(self.sr*1.5):self.sr*3])

    def test_negative_indexing_with_padding_and_step(self):
        conc = np.zeros((self.sr))
        def concat(arr):
            return np.concatenate((arr, conc))
        
        np.testing.assert_array_equal(self.track[-500:self.sr * 3], concat(self.signal)[-500 - self.sr:self.sr * 3])
        np.testing.assert_array_equal(self.track[-500000:self.sr * 3], concat(self.signal)[-500000 - self.sr:self.sr * 3])
        np.testing.assert_array_equal(self.track[-1:self.sr * 3], concat(self.signal)[-1 - self.sr:self.sr * 3])