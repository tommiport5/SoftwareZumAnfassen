import time
from region import Region
from strip import Strip
from hw_interface import clear, set_pixel, show

NUM_LEDS = 8
positions = [2.5, 3.5, 6.5]
deltas = [0.08, 0.06, -0.07]
# Region test
ids = [None] * 3
s = Strip(NUM_LEDS)

def makeRegion(ind,col,wdt=None,brn=None):
    global ids
    ids[ind] = s.newRegion(positions[ind], colspec=col, width=wdt, br=brn)
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
    arr = s.to_uint32arr()
    for i in range(NUM_LEDS):  
        set_pixel(i, arr[i])
    show()
    
def change():
    global ids
    # activate one, deactivate another
    for k in range(3):
        if ids[k] is None:
            ids[k] = s.newRegion(positions[k], br=3)
            break
    for l in range(k+1, k+4):
        m = l % 3
        if ids[m] is not None:
            s.removeRegion(ids[m])
            ids[m] = None
            break
            
    
makeRegion(0, "red", brn=9)
display()
time.sleep(5)
delRegion(0)
makeRegion(1, "green", wdt=5)
display()
time.sleep(5)
delRegion(1)
makeRegion(2, "blue", brn=9)
display()
time.sleep(5)
makeRegion(0, "red", brn=9)
j = 0
while (True):
    j += 1
    if j % 100 == 0: change()
    for i in range(3):
        if ids[i]:
            positions[i] = (positions[i] + deltas[i]) % 8
            # print(positions[i])
            s.moveRegion(ids[i], positions[i])
    display()
    time.sleep_ms(50)

while sm.tx_fifo() > 0:
    pass
