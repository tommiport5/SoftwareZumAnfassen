"""
class LED
Software representation for a LED
"""
from color import color


class LED:
    def __init__(self, colspec, offset=0.0):
        self._color = color(colspec)
        self._offset = offset

    def __str__(self):
        return str(self._color)

    # value comparison
    def __eq__(self, other):
        return self._color == other.color
    
    @property
    def color(self):
        return self._color    
        
    def copy(self):
        return LED(self._cols, self._offset)
    
    def mult(self, fac):
        new_led = LED([c*fac for c in self._color.value])
        new_led._rescale()
        return new_led

    def add(self, other):
        new_led = LED([c+o for (c, o) in zip(self._color.value, other._color.value)])
        new_led._rescale()
        return new_led

    def move(self, fr):
        if fr < 0. or fr >= 1.: raise ValueError
        self._offset = fr

    # keep the numeric values in range 0.0 < v <= 1.0
    def _rescale(self):
        if self._color == color("black"): return
        mn = min(self._color.value)
        if (mn < 0.0):
            self._color = color([ c + mx for c in self._color.value])
        mx = max(self._color.value)
        if (mx > 1.0):
            self._color = color([ c / mx for c in self._color.value])
 

