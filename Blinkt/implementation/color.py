"""
color.py
representation of color
"""
from random import randrange as rr
import sys

# Color values are rgb tuples
_cols = {
    "red":   [v/255. for v in (0xff, 0, 0)],
    "green": [v/255. for v in (0, 0xff, 0)],
    "blue":  [v/255. for v in (0, 0, 0xff)],
    "black": [v/255. for v in (0, 0, 0)],
    "magenta": [v/255. for v in (168, 50, 162)],
    "yellow": [v/255. for v in (222, 242, 44)],
    "purple": [v/255. for v in (123, 44, 242)],
    "pink": [v/255. for v in (242, 44, 176)],
    "turquoise": [v/255. for v in (44, 242, 235)],
    "orange": [v/255. for v in (242, 169, 44)]
    }
    
class color:
    def __init__(self, colspec=None):
        if colspec is None:
            self._value = list(_cols.values())[rr(len(_cols))]
        elif isinstance(colspec, list): 
            self._value = colspec
        elif colspec in _cols:
            self._value = _cols[colspec]
        else:
            raise TypeError

    @property
    def value(self):
        return self._value

    # make this a copy if necessary
    @value.setter
    def value(self, val):
        self._value = val
        
    def __eq__(self, other):
        return all(abs(s-o) < 4e-9 for (s,o) in zip(self._value, other._value))

    def __str__(self):
        return "".join("%f " % c for c in self._value)

if __name__ == "__main__":
        that = color()
        print(that)
        print(color("magenta") == color("magenta"))
        print(color("magenta") == color("green"))
        for (name, val) in _cols.items():
                if color(val) == that:
                        print(name)
                        break
        print(color([0.1, 0.2, 0.3]))
        print(color("pink"))
        
