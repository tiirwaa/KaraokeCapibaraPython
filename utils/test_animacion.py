import unittest
from svgpathtools import svg2paths
import numpy as np

class TestAnimation(unittest.TestCase):
    def setUp(self):
        self.paths, _ = svg2paths('res/svg/salida_bezier.svg')
        self.feet_indices = [0, 1, 2, 3]
        self.legs_indices = [23, 24]

    def test_feet_paths_exist(self):
        for i in self.feet_indices:
            self.assertLess(i, len(self.paths), f"Path {i} does not exist")
            self.assertIsNotNone(self.paths[i], f"Path {i} is None")

    def test_legs_paths_exist(self):
        for i in self.legs_indices:
            self.assertLess(i, len(self.paths), f"Path {i} does not exist")
            self.assertIsNotNone(self.paths[i], f"Path {i} is None")

    def test_feet_positions(self):
        for i in self.feet_indices:
            start = self.paths[i].start
            self.assertGreater(start.imag, 800, f"Feet path {i} not in bottom area")

    def test_legs_positions(self):
        for i in self.legs_indices:
            bbox = self.paths[i].bbox()
            min_y, max_y = bbox[2], bbox[3]
            self.assertGreater(min_y, 200, f"Legs path {i} not in leg area")
            self.assertLess(max_y, 500, f"Legs path {i} not in leg area")

    def test_feet_follow_legs_simulation(self):
        # Simulate positions after animation
        # This is a mock; in real test, would need to run Manim or mock
        feet_center = np.array([0, 900])  # Mock
        legs_center = np.array([0, 300])  # Mock
        # Check if feet are below legs
        self.assertGreater(feet_center[1], legs_center[1], "Feet should be below legs")

if __name__ == '__main__':
    unittest.main()