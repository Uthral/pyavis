import numpy as np
from unittest import TestCase
from pyavis.shared.multitrack import Track 
from pyavis.shared import Signal

class TestTrack(TestCase):
    def test_get_index(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig1 = Signal(val)
        sig2 = Signal(val)

        track.try_add(0, sig1)
        track.try_add(500, sig2)
        idx1 = track.get_index(0, sig1)
        idx2 = track.get_index(500, sig2)

        self.assertEqual(idx1, 0)
        self.assertEqual(idx2, 1)

    def test_get_signal_at_position(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig = Signal(val)

        track.try_add(0, sig)
        result = track.get_signal_at_position(20)

        self.assertIsNotNone(result)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], sig)

    def test_get_signal_at_position_none(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig = Signal(val)

        track.try_add(0, sig)
        result = track.get_signal_at_position(5000)

        self.assertIsNone(result)

    def test_remove(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig1 = Signal(val)
        sig2 = Signal(val)

        track.try_add(0, sig1)
        track.try_add(500, sig2)

        self.assertEqual(len(track.signals), 2)
        track.remove(0, sig1)
        self.assertEqual(len(track.signals), 1)
        track.remove(500, sig2)
        self.assertEqual(len(track.signals), 0)

    def test_add_signal(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig = Signal(val)

        result = track.try_add(0,sig)

        self.assertTrue(result)
        self.assertEqual(len(track.signals), 1)

    def test_add_multile_signals(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig1 = Signal(val)
        sig2 = Signal(val)

        result1 = track.try_add(0, sig1)
        result2 = track.try_add(200, sig2)

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertEqual(len(track.signals), 2)
    
    def test_add_overlaping_signals(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig1 = Signal(val)
        sig2 = Signal(val)

        result1 = track.try_add(0, sig1)
        result2 = track.try_add(50, sig2)

        self.assertTrue(result1)
        self.assertFalse(result2)
        self.assertEqual(len(track.signals), 1)

    def test_move_signal(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig1 = Signal(val)
        sig2 = Signal(val)

        track.try_add(0, sig1)
        track.try_add(200, sig2)
        idx = track.get_index(0, sig1)

        result1 = track.try_move(500, idx)
        result2 = track.get_signal_at_position(500)

        self.assertTrue(result1)
        self.assertIsNotNone(result2)
        self.assertEqual(result2[0], 500)
        self.assertEqual(result2[1], sig1)

    def test_move_overlapping_signal(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig1 = Signal(val)
        sig2 = Signal(val)

        track.try_add(0, sig1)
        track.try_add(200, sig2)
        idx = track.get_index(0, sig1)

        result1 = track.try_move(250, idx)
        result2 = track.get_signal_at_position(0)

        self.assertFalse(result1)
        self.assertIsNotNone(result2)
        self.assertEqual(result2[0], 0)
        self.assertEqual(result2[1], sig1)

    def test_get_section(self):
        track = Track()
        val = np.linspace(0, np.pi, 100)
        sig = Signal(val)

        track.try_add(50, sig)
        section1 = track.get_section(0, 50)
        section2 = track.get_section(50, 150)
        section3 = track.get_section(0, 150)

        np.testing.assert_array_equal(np.zeros(50), section1)
        np.testing.assert_array_equal(val, section2)
        np.testing.assert_array_equal(np.concatenate((np.zeros(50), val)), section3)

        


    


        


