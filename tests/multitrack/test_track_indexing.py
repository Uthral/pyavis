import numpy as np
from unittest import TestCase
from pyavis.shared.multitrack import Track

from pya import Asig
from pyavis.shared import AudioSignal

class TestTrackIndexing(TestCase):
    def setUp(self) -> None:
        self.sr = 44100
        self.val_1 = np.sin(2 * np.pi * 50 * np.linspace(0, 1, self.sr), dtype="float32")
        self.val_2 = np.sin(2 * np.pi * 50 * np.linspace(0, 1, self.sr), dtype="float32")
        self.sig_1 = AudioSignal(Asig(self.val_1))
        self.sig_2 = AudioSignal(Asig(self.val_2))
        self.pos_1 = 0
        self.pos_2 = self.sr * 3

        zeros = np.zeros((self.sr * 2 - self.pos_1))
        self.concat = np.concatenate(([0] * self.pos_1, self.val_1, zeros, self.val_2))
        self.concat_with_padding = np.concatenate((self.concat, zeros))

        self.track = Track("Test", self.sr)
        self.track.try_add(self.pos_1, self.sig_1)
        self.track.try_add(self.pos_2, self.sig_2)

        self.assert_func = np.testing.assert_array_equal

    def test_invalid_indexing(self):
        with self.assertRaises(TypeError):
            self.track[1]
        
        with self.assertRaises(TypeError):
            self.track["a"]
        
        with self.assertRaises(TypeError):
            self.track[[1,2,3]]
    
    def test_positive_indexing(self):
        self.assert_func(self.track[self.pos_1:self.pos_1 + 5000], self.val_1[0:5000])
        self.assert_func(self.track[self.pos_1 + 5000:self.pos_1 + 5000], self.val_1[5000:5000])
        self.assert_func(self.track[self.pos_1:self.pos_1 + len(self.val_1)], self.val_1[:])

    def test_negative_indexing(self):
        self.assert_func(self.track[0:20], self.concat[0:20])
        self.assert_func(self.track[0:-100], self.concat[0:-100])
        self.assert_func(self.track[::-1], self.concat[::-1])
    
    def test_indexing_with_step(self):
        for i in range(1, 50, 1):
            self.assert_func(self.track[self.pos_1:self.pos_1 + 100:i], self.concat[self.pos_1:self.pos_1 + 100:i])
            self.assert_func(self.track[self.pos_1 + 100:self.pos_1 + 5000:i], self.concat[self.pos_1 + 100:self.pos_1 + 5000:i])
            self.assert_func(self.track[::i], self.concat[::i])

        for i in range(-1, -50, -1):
            self.assert_func(self.track[self.pos_1 + 100:self.pos_1:i], self.concat[self.pos_1 + 100:self.pos_1:i])
            self.assert_func(self.track[self.pos_1 + 5000:self.pos_1 + 100:i], self.concat[self.pos_1 + 5000:self.pos_1 + 100:i])
            self.assert_func(self.track[::i], self.concat[::i])

    def test_positive_indexing_with_padding(self):
        self.assert_func(self.track[:], self.concat[:])
        self.assert_func(self.track[self.sr:self.sr * 3], self.concat[self.sr:self.sr * 3])
        self.assert_func(self.track[self.sr * 2:self.sr * 3], self.concat[self.sr * 2:self.sr * 3])
        self.assert_func(self.track[self.pos_2 + len(self.val_2):self.pos_2 + len(self.val_2) + self.sr], self.concat_with_padding[self.pos_2 + len(self.val_2):self.pos_2 + len(self.val_2) + self.sr])

    def test_indexing_with_padding_and_step(self):
        for i in range(1, 50, 1):
            # Get entire track values
            self.assert_func(self.track[::i], self.concat[:self.track.get_minimum_length():i])
            # Start after first signal and stop at second signal
            self.assert_func(self.track[self.pos_1 + len(self.val_1):self.pos_2:i], self.concat[self.pos_1 + len(self.val_1):self.pos_2:i])
            # Start outside of second signal and stop at the end of second signal
            self.assert_func(self.track[self.pos_2-100:self.pos_2 + len(self.val_2):i], self.concat[self.pos_2-100:self.pos_2 + len(self.val_2):i])
            # Start inside of second signal and stop inside of second signal
            self.assert_func(self.track[self.pos_2:self.pos_2 + 100:i], self.concat[self.pos_2:self.pos_2 + 100:i])
            # Go over the length of the track
            self.assert_func(self.track[self.pos_2 + len(self.val_2):self.pos_2 + len(self.val_2) + self.sr:i], self.concat_with_padding[self.pos_2 + len(self.val_2):self.pos_2 + len(self.val_2) + self.sr:i])

        for i in range(-1, -50, -1):
            # Get entire track values
            self.assert_func(self.track[::i], self.concat[::i])
            # Start at second signal and get until end of first signal
            self.assert_func(self.track[self.pos_2:self.pos_1 + len(self.val_1):i], self.concat[self.pos_2:self.pos_1 + len(self.val_1):i])
            # Start outside of second signal and stop at the start of second signal
            self.assert_func(self.track[self.pos_2 + len(self.val_2) + 100:self.pos_2:i], self.concat_with_padding[self.pos_2 + len(self.val_2) + 100:self.pos_2:i])
            # Start inside of second signal and stop inside of second signal
            self.assert_func(self.track[self.pos_2 + 100:self.pos_2:i], self.concat[self.pos_2 + 100:self.pos_2:i])
            # Go over the length of the track
            self.assert_func(self.track[self.pos_2 + len(self.val_2) + self.sr:self.pos_2 + len(self.val_2):i], self.concat_with_padding[self.pos_2 + len(self.val_2) + self.sr:self.pos_2 + len(self.val_2):i])

    def test_time_indexing(self):
        self.assert_func(self.track[{1:2}], self.concat[self.sr:self.sr*2])

    def test_time_indexing_with_padding_and_step(self):
        self.assert_func(self.track[{1:3}], self.concat[self.sr:self.sr*3])
        self.assert_func(self.track[{1.5:3}], self.concat[int(self.sr*1.5):self.sr*3])