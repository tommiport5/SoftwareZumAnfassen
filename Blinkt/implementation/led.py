"""
class LED
Software representation for a LED
"""
from random import randrange as rr
import math

DEFAULT_BRIGHTNESS = 7

# Color values are rgb tuples
_cols = {
    "red":   [0xff, 0, 0],
    "green": [0, 0xff, 0],
    "blue":  [0, 0, 0xff],
    "black": [0, 0, 0],
    "magenta": [168, 50, 162],
    "yellow": [222, 242, 44],
    "purple": [123, 44, 242],
    "pink": [242, 44, 176],
    "turquoise": [44, 242, 235],
    "orange": [242, 169, 44]
    }

class LED:
    def __init__(self, colspec, br=DEFAULT_BRIGHTNESS, offset=0.0):
        if colspec is None:
            cols = list(_cols.values())[rr(len(_cols))]
        elif isinstance(colspec, list): 
            cols = colspec
        elif colspec in _cols:
            cols = _cols[colspec]
        else:
            raise TypeError
        self._cols = cols
        self._br = float(DEFAULT_BRIGHTNESS) if br is None else float(br)
        self._offset = offset

    def __str__(self):
        return "0x%x" % self.to_uint32()

    # value comparison
    def __eq__(self, other):
        fac = self._br / other._br
        cmp = [min(round(fac*v), 255) for v in self._cols]
        for i in range(3):
            if other._cols[i] != cmp[i]:
                print(self, cmp)
                return False
        else:
            return True
        
    def copy(self):
        return LED(self._cols,self._br, self._offset)
    
    # try to keep the numeric values in good range
    def _rescale(self):
        mx = max(self._cols)
        if mx == 0 or self._br == 0: return
        # the maximum *should* have a value of 20 at least
        fac = 20. / mx
        new_br = self._br / fac
        if mx < 20 and new_br >= 1:
            # the maximum is low, but we can increase it by reducing the brightness
            self._br = new_br
            for i in range(len(self._cols)):
                self._cols[i] = round(self._cols[i] * fac)
            # recalc maximum
            mx = max(self._cols)
        if mx > 255:
            # we *must* limit the max cols
            minfac = mx / 255.0
            maxfac = 31.0 / self._br
            # if minfac <= maxfac, it is sufficient
            fac = min(minfac, maxfac)
            self._br = self._br * fac
            for i in range(len(self._cols)):
                self._cols[i] = round(self._cols[i] / fac)
            # in any case we cut at 255              
            for i in range(len(self._cols)):
                if self._cols[i] > 255: self._cols[i] = 255
    
    def mult(self, fac):
        new_led = LED([round(c*fac) for c in self._cols], self._br)
        new_led._rescale()
        return new_led

    def add(self, other):
        if self._br > other._br:
            mul = self._br / other._br 
            new_led = LED([round(self._cols[i] * mul) + other._cols[i] for i in range(len(self._cols))], other._br)
        elif other._br > self._br:
            mul = other._br / self._br 
            new_led = LED([self._cols[i] + round(other._cols[i] * mul) for i in range(len(self._cols))], self._br)
        else:
            new_led = LED([self._cols[i] + other._cols[i] for i in range(len(self._cols))], self._br)
        new_led._rescale()
        return new_led

    def move(self, fr):
        if fr < 0. or fr >= 1.: raise ValueError
        self._offset = fr

    #convert self into a 32bit value suitable for apa102
    def to_uint32(self):
        return (self._cols[2] & 0xff) << 16 | (self._cols[1] & 0xff) << 8 | self._cols[0] & 0xff | (round(self._br) & 0x1f | 0xe0)  << 24
