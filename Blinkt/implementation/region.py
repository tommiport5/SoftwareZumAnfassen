""" class Region
Defines a region of light that can interact with other regions
and can be shown.
"""
from random import randrange as rr
import math
from led import LED


class Region:
    def __init__(self, offset, colspec=None, width=3):
        if width is None: width = 3
        self._width = (width-1) | 1
        self._pure = LED(colspec)
        self._offset = offset
        # experimentally found for Strips of 8 Leds
        self._factor = self._width / (3.0*7.0)

    def __len__(self):
        return self._width+1
        
    def move(self, offset):
        if offset < 0. or offset >= 1.0: raise ValueError
        self._offset = offset

    def mult(self, factor):
        self._pure = self._pure.mult(factor)
        return(max(self._pure.color.value))
    
    def to_LedArray(self):
        arr = [LED("black")] * len(self)
        ci = self._width//2
        lower = self._pure.mult(1.0 - self._offset + self._factor*self._offset)
        higher = self._pure.mult(self._factor + self._offset - self._factor * self._offset)
        arr[ci] = lower
        arr[ci+1] = higher
        for i in range(ci-1, -1, -1):
            lower = lower.mult(self._factor)
            arr[i] = lower
        for i in range(ci+2, len(arr)):
            higher = higher.mult(self._factor)
            arr[i] = higher
        return arr

            
         
        
        

