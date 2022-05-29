# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random

pixels = neopixel.NeoPixel(board.D18, 6)

class Pixel:
  def __init__(self, index, g, b):
    self.index = index
    self.g = g
    self.b = b

  def colorPixel(self):
    time.sleep(0.03)

    pixels[self.index] = (0, self.g, self.b)

  p0 = Pixel(0, random.randint(100, 255), random.randint(100, 255))
  p1 = Pixel(1, random.randint(100, 255), random.randint(100, 255))

while True:
  p0.colorPixel()
  p1.colorPixel()
