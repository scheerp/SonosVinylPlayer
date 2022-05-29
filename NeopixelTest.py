# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 6

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.4, auto_write=False, pixel_order=ORDER
)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    print(pos)
    if pos < 100 or pos > 255:
        g = b = 100
    elif pos < 100:
        g = int(255 - pos)
        b = 100
    elif pos < 170:
        pos -= 100
        g = 100
        b = int(pos)
    else:
        pos -= 170
        g = int(pos)
        b = int(255 - pos)
    return (0, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (0, g, b, 0)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(random.randint(0, num_pixels - 1) & 255)
        pixels.show()
        time.sleep(wait)


while True:
    rainbow_cycle(0.03)  # rainbow cycle with 1ms delay per step
