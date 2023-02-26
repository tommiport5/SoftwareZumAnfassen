"""
apa102_interface
implements the led_interface for the apa102 led

TODO: reduce the amount of copies for the led values

Note: Python doesn't have interfaces or abstract base classes,
so the led_interface exists only in the design
"""

from hw_interface import clear, show, set_pixel
from color import color
import math

# the highest possible brightness for one color
# this corresponds to a color value of 1.0
MAX_TOTAL = 0xff * 0x1e

def clear():
    print("clear")


class apa102_interface:
    @classmethod
    def clear(cls):
        clear()
    
    @classmethod
    def show(cls):
        show()

    """ set_pixels main task is to convert a color value to
    a uint32_t suitable for the apa102. The strategy is to use
    the least possible brightness to achieve the color value
    col[i] * MAX-TOTAL
    """
    @classmethod
    def set_pixel(cls, i, col):
        if col == color("black"):
            pv = 0xe0_000000
            # return "black"
        else:
            # this is what we must reach
            bright = math.ceil(max(col.value)*31.0)
            intens = [ int(c * 255) for c in col.value]
            pv = (0xe0 | bright) << 24 | (intens[2] & 0xff) << 16 | (intens[1] & 0xff ) << 8 | (intens[0] & 0xff)
            # return (intens, bright)
        set_pixel(i, pv)

if __name__ == "__main__":
    from color import _cols
    for (n, c) in _cols.items():
        print(n, apa102_interface.set_pixel(0, color(c)))
