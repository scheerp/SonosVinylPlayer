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
    pixels[self.index] = (0, self.g, self.b)


while True:
  p0 = Pixel(0, 100, 150)
  p0.colorPixel()

  p1 = Pixel(1, 255, 100)
  p1.colorPixel()
