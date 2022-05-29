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
pixels[0] = (100, 150, 200)

class Pixel:
  def __init__(self, index, g, b):
    self.index = index
    self.g = g
    self.b = b

  def colorPixel(self):
    print(self.index, self.g, self.b)
    pixels[self.index] = (0, self.g, self.b)


while True:
  p0 = Pixel(0, 100, 150)
  p0.colorPixel()

  p1 = Pixel(1, 255, 100)
  p1.colorPixel()
