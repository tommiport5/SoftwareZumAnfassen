"""
  Unittests for the Led module
"""
import unittest
import sys
from pathlib import Path
sys.path.append(str(Path.cwd().joinpath("..", "implementation")))
from led import LED

class TestLED(unittest.TestCase):
    def test_basics(self):
        self.assertEqual(LED("green").to_uint32(), 0xe700ff00)

    def test_str(self):
        self.assertEqual(str(LED("black")), "0xe7000000")

    def test_mult(self):
        self.assertEqual(LED("red").mult(0.5).to_uint32(), 0xe7000080)

    def test_add(self):
        self.assertEqual(LED("blue").add(LED("green")).to_uint32(), 0xe7ffff00)
        
    def test_add_1(self):
        self.assertEqual(LED("red").add(LED("black")), LED("red"))

    def test_rescale_down(self):
        led = LED([0, 0x17f, 0])
        led._rescale()
        self.assertEqual(led.to_uint32(), 0xeb00ff00)

    def test_rescale_up(self):
        led = LED([0, 0, 10], 14)
        led._rescale()
        self.assertEqual(led.to_uint32(), 0xe7140000)

    def test_rescale_rev_down(self):
        orig = LED([0,0,20], 31)
        for i in range(30, 21, -1):
            fac = float(i) / 31.
            self.assertEqual(orig.mult(fac).mult(1./fac), orig)

if __name__ == "__main__":
    unittest.main()
        
