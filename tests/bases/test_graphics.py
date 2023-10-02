from unittest import TestCase
from pyavis.backends.bases.graphic_bases import *

import numpy as np

class TestGraphicBases(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_graphic_element(self):
        e = GraphicElement((0,0), True)
        self.assertEqual(e.position, (0,0))
        self.assertEqual(e.active, True)

        e.set_active(False)
        e.set_position(1, 1)
        self.assertEqual(e.position, (1,1))
        self.assertEqual(e.active, False)

    def test_layout(self):
        l = Layout()
        l.add_track("test", 0, 0)

    def test_layout_mulitple(self):
        l = Layout(2,2)
        l.add_track("test 1", 0, 0)
        l.add_track("test 2", 0, 1)
        l.add_track("test 3", 1, 0)
        l.add_track("test 4", 1, 1)

    def test_layout_outside_of_range(self):
        l = Layout(2,2)

        values = [
            ("test 1", -1, 0),
            ("test 2", 0, -1),
            ("test 3", -1, -1),
            ("test 4", 0, 2),
            ("test 5", 2, 0),
            ("test 6", 2, 2),
        ]
        for v in values:
            with self.assertRaises(ValueError):
                l.add_track(*v)

    def test_layout_span_invalid(self):
        l = Layout(2,2)

        values = [
            ("test 1", 0, 0, 3, 1),
            ("test 2", 0, 0, 1, 3),
            ("test 3", 0, 0, 3, 3),
            ("test 4", 0, 0, -1, 1),
            ("test 5", 0, 0, 1, -1),
            ("test 6", 0, 0, -1, -1),
        ]

        for v in values:
            with self.assertRaises(ValueError):
                l.add_track(*v)

    def test_signal(self):
        x = np.arange(100)
        y = np.zeros((100))

        values = [
            [((0,0), 1, y), {}],
            [((0,0), 1, x, y), {}],
            [((0,0), 1, (y)), {}],
            [((0,0), 1, (y,)), {}],
            [((0,0), 1, (x,y)), {}],
            [((0,0), 1), {'x': x, 'y': y}],
        ]

        for args, kwargs in values:
            s = Signal(*args, **kwargs)
            self.assertEqual(len(s.x_data), len(s.y_data))
    
    def test_signal_length_missmatch(self):
        x = np.arange(100)
        y = np.zeros((90))

        values = [
            [((0,0), 1, x, y), {}],
            [((0,0), 1, (x,y)), {}],
            [((0,0), 1), {'x': x, 'y': y}],
        ]

        for args, kwargs in values:
            with self.assertRaises(ValueError):
                s = Signal(*args, **kwargs)
    
    def test_signal_size(self):
        x = np.arange((100))
        y = np.ones((100))

        values = [
            [((0,0), 2.0, y), {}, 2.0],
            [((0,0), 4.0, x, y), {}, 4.0],
            [((0,0), 8.0, (y)), {}, 8.0],
            [((0,0), 16.0, (y,)), {}, 16.0],
            [((0,0), 32.0, (x,y)), {}, 32.0],
            [((0,0), 64.0), {'x': x, 'y': y}, 64.0],
        ]

        for args, kwargs, size in values:
            s1 = Signal(*args, **kwargs)
            np.testing.assert_array_equal(s1.y_data_scaled, y * size)

            s1.set_scale(size * 2)
            np.testing.assert_array_equal(s1.y_data_scaled, y * size * 2)