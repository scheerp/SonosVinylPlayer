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
    
    g_factor = -3
    b_factor = 3
    
    if self.g < 0:
      g_factor = 3
    if self.g > 255:
      g_factor = -3
    
    if self.b < 0:
      b_factor = 3
    if self.b > 255:
      b_factor = -3

    self.g += g_factor
    self.b += b_factor

    pixels[self.index] = (0, self.g, self.b)

p0 = Pixel(0, random.randint(100, 255), random.randint(100, 255))
p1 = Pixel(1, random.randint(100, 255), random.randint(100, 255))
p2 = Pixel(0, random.randint(100, 255), random.randint(100, 255))
p3 = Pixel(1, random.randint(100, 255), random.randint(100, 255))
p4 = Pixel(0, random.randint(100, 255), random.randint(100, 255))
p5 = Pixel(1, random.randint(100, 255), random.randint(100, 255))

while True:
  p0.colorPixel()
  p1.colorPixel()
  p2.colorPixel()
  p3.colorPixel()
  p4.colorPixel()
  p5.colorPixel()
