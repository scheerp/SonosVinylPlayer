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
    self.g_factor =random.randint(-5, 5)
    self.b_factor =random.randint(-5, 5)

  def colorPixel(self):
    if self.b_factor == 0:
      self.b_factor +=1

    if self.g_factor == 0:
      self.g_factor += 1
    
    if self.g < 30 or self.g > 240:
      self.g_factor = self.g_factor * -1
    
    if self.b < 50 or self.b > 240:
      self.b_factor = self.b_factor * -1

    self.g += self.g_factor
    self.b += self.b_factor
    pixels[self.index] = (0, self.g, self.b)
    print('G:', self.g, 'GFACTOR:', self.g_factor)
    time.sleep(0.05)

p0 = Pixel(0, 5, 5)
p1 = Pixel(1, 5, 5)
p2 = Pixel(2, 5, 5)
p3 = Pixel(3, 5, 5)
p4 = Pixel(4, 5, 5)
p5 = Pixel(5, 5, 5)

while True:
  p0.colorPixel()
  p1.colorPixel()
  p2.colorPixel()
  p3.colorPixel()
  p4.colorPixel()
  p5.colorPixel()

GPIO.cleanup()
