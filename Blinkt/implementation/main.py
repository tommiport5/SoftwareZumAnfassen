import time
#from enum import Enum
from region import Region
from strip import Strip
from apa102_interface import apa102_interface

NUM_LEDS = 8
positions = [2.5, 3.5, 6.5] 
deltas = [0.08, 0.06, -0.07]
# Region test
ids = [None] * 3
s = Strip(NUM_LEDS)

def makeRegion(ind,col,wdt=None):
    global ids
    ids[ind] = s.newRegion(positions[ind], colspec=col, width=wdt)
    # print("make", ind, ids)
    
def delRegion(ind):
    global ids
    # print("del", ind, ids)
    s.removeRegion(ids[ind])
    ids[ind] = None
    
def moveRegion(ind):
    global positions
    positions[ind] = (positions[ind] + deltas[ind]) % 8
    
def display():
    arr = s.complete()
    for i in range(NUM_LEDS):  
        apa102_interface.set_pixel(i, arr[i].color)
    apa102_interface.show()
    
class change:
    #class State(Enum):
    FADE_IN = 1
    FADE_OUT = 2
    NO_CHANGE = 3
        
    def __init__(self, strip, ids):
        self._strip = strip
        self._ids = ids
        self._cnt = 0
        self._k = 0
        self._state = self.NO_CHANGE
        self._orig = 0.0
        
    def __call__(self):
        if self._state == self.NO_CHANGE:
            self._cnt += 1
            if self._cnt % 100 == 0:
                self._start_out()
                return True
            else:
                return False
        elif self._state == self.FADE_OUT:
            val = self._strip.multRegion(self._ids[self._k], 0.9)
            # print("fo", val)
            if val < 0.1:
                self._start_in()
            return True
        elif self._state == self.FADE_IN:
            val = self._strip.multRegion(self._ids[self._k], 1.5)
            # print("fi", val)
            if val >= self._orig:
                self._state = self.NO_CHANGE
                return False
            return True
    
    def _start_out(self):
        # deactivate one with fade out
        for k in range(self._k+1,self._k+4):
            m = k % 3
            if not ids[m] is None:
                self._k = m
                self._state = self.FADE_OUT
                break
        # print("so", self._k)
            
    def _start_in(self):
        # faded out, now activate a new one
        delRegion(self._k)
        makeRegion(self._k, None)
        self._orig = self._strip.multRegion(self._ids[self._k], 1.0)
        self._strip.multRegion(self._ids[self._k], 0.01)
        self._state = self.FADE_IN
        # print("si", self._k)
   
makeRegion(0, "red")
display()
time.sleep(5)
delRegion(0)
makeRegion(1, "green", wdt=5)
display()
time.sleep(5)
delRegion(1)
makeRegion(2, "blue")
display()
time.sleep(5)
makeRegion(0, "red")
chg = change(s, ids)
while (True):
    if not chg():
        for i in range(3):
            if ids[i]:
                positions[i] = (positions[i] + deltas[i]) % 8
                # print(positions[i])
                s.moveRegion(ids[i], positions[i])
    display()
    time.sleep_ms(50)
