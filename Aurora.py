# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
#!/usr/bin/env python

import RPi.GPIO as GPIO
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
    self.g_factor =-3
    self.b_factor =3

  def colorPixel(self):
    
    if self.g < 100 or self.g > 240:
      self.g_factor = self.g_factor * -1
    
    if self.b < 100 or self.b > 240:
      self.b_factor = self.b_factor * -1

    self.g += self.g_factor + random.randint(1, 3)
    self.b += self.b_factor
    pixels[self.index] = (0, self.g, self.b)
    print('G:', self.g, 'GFACTOR:', self.g_factor)
    time.sleep(0.05)

p0 = Pixel(0, random.randint(100, 240), random.randint(100, 240))
# p1 = Pixel(1, random.randint(100, 240), random.randint(100, 240))
# p2 = Pixel(2, random.randint(100, 240), random.randint(100, 240))
# p3 = Pixel(3, random.randint(100, 240), random.randint(100, 240))
# p4 = Pixel(4, random.randint(100, 240), random.randint(100, 240))
# p5 = Pixel(5, random.randint(100, 240), random.randint(100, 240))

while True:
  p0.colorPixel()
  # p1.colorPixel()
  # p2.colorPixel()
  # p3.colorPixel()
  # p4.colorPixel()
  # p5.colorPixel()

GPIO.cleanup()
