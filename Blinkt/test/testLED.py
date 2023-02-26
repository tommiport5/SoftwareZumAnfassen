"""
  Unittests for the Led module
"""
import unittest
import sys
from pathlib import Path
sys.path.append(str(Path.cwd().joinpath("..", "implementation")))
from led import LED
from color import color

class TestLED(unittest.TestCase):
    def test_basics(self):
        self.assertEqual(LED("green"), LED([0.0, 1.0, 0.0]))

    def test_str(self):
        self.assertEqual(str(LED("black")), "0.000000 0.000000 0.000000 ")

    def test_mult(self):
        self.assertEqual(LED("red").mult(0.5), LED([0.5, 0, 0]))

    def test_add(self):
        self.assertEqual(LED("blue").add(LED("green")), LED([0, 1.0, 1.0]))
        
    def test_add_1(self):
        self.assertEqual(LED("red").add(LED("black")), LED("red"))

    def test_rescale_down(self):
        led = LED([0, 1.01, 0])
        led._rescale()
        self.assertEqual(led.color, color([0, 1, 0]))

    def test_rescale_up(self):
        led = LED([0, 0, 0.2])
        led._rescale()
        self.assertEqual(str(led.color), "0.000000 0.000000 0.200000 ")

    def test_rescale_rev_down(self):
        orig = LED([0.4,0.3,0.2])
        for i in range(30, 0, -1):
            fac = float(i) / 31.
            self.assertEqual(orig.mult(fac).mult(1./fac), orig)

if __name__ == "__main__":
    unittest.main()
        
