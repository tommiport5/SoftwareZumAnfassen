from machine import Pin
from time import sleep_ms as sleep

# to remind us which pin serves which function
DAT = Pin(16, Pin.OUT)
CLK = Pin(17, Pin.OUT)
# number of pixels in the chain
NUM_PIXELS = 8
# default brightness setting
BRIGHTNESS = 7
# list of pixels
pixels = [0xe000000] * NUM_PIXELS

# Set the brightness of all pixels - 0 - 1.
def set_brightness(brightness):
    if brightness < 0 or brightness > 1:
        return
    for x in range(NUM_PIXELS):
        pixels[x][3] = int(31.0 * brightness) & 0b11111

# Clear all of the pixels       
def clear():
    global pixels
    pixels = [0xe000000] * NUM_PIXELS

# Latch procedure - 36 clock pulses        
def eof():
    DAT.value(1)
    for x in range(36):
        CLK.value(1)
        CLK.value(0)

# Latch at start - 32 clock pulses    
def sof():
    DAT.value(0)
    for x in range(32):
        CLK.value(1)
        CLK.value(0)

# Update colour and brightness values from pixels list
# Call this procedure to update the display
def show():
    sof()
    for pixel in pixels:
        mask = 1 << 31
        for _ in range(32):
            DAT.value(pixel & mask)
            CLK.value(1)
            CLK.value(0)
            mask >>= 1
    eof()


# Set the uint_32 value for a pixel
def set_pixel(i, val):
    pixels[i] = val

if __name__ == "__main__":
    def set_all(val):
        global pixels
        pixels = [val for _ in pixels]
        
    while True:
        # all off
        clear()
        show()
        sleep(1000)
        # on red individually
        for i in range(NUM_PIXELS):
            set_pixel(i,0xe700_00ff)
            show()
            sleep(100)        
        sleep(1000)
        # all green
        set_all(0xe700_ff00)
        show()
        sleep(1000)
        # all blue
        clear()
        set_all(0xe7ff_0000)
        show()
        sleep(1000)
