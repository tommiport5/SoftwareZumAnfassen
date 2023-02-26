"""
class Strip
Software representation of the whole strip of LEDs
"""

import math
from led import LED
from region import Region


class Strip:
    def __init__(self, num):
        self._num = num
        self._regions = {}
        self._last = 0
        
    # add a region and return its id
    def newRegion(self, pos, width=3, colspec=None):
        if pos < 0: raise ValueError
        (ifr, ipos) = math.modf(pos)
        if ipos >= self._num: raise ValueError
        id = self._last
        self._last += 1 # not reentrant, but we are only single threaded
        self._regions.update({id: [int(ipos), Region(ifr, width=width, colspec=colspec)]})
        return id

    def moveRegion(self, id, pos):
        if pos < 0: raise ValueError
        [ifr, ipos] = math.modf(pos)
        if ipos >= self._num: raise ValueError
        self._regions[id][1].move(ifr)
        self._regions[id][0] = int(ipos)

    def multRegion(self, id, factor):
        return self._regions[id][1].mult(factor)
        
    def removeRegion(self, id):
        del self._regions[id]

    def complete(self):
        arr = [LED("black") for v  in range(self._num)]
        for [ipos, reg] in iter(self._regions.values()):
            la = reg.to_LedArray()
            for i in range(len(la)):
                ti = (i + ipos - len(la)//2)%len(arr) 
                # print(i, la[i], arr[ti])
                arr[ti] = arr[ti].add(la[i])
                # print(ti, arr[ti])
                arr[ti]._rescale()
        return arr

if __name__ == "__main__":
    s = Strip(8)
    id = s.newRegion(3.06, colspec="red")
    for x in s.complete():
        print(x)

