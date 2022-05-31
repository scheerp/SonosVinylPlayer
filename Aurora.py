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
  def __init__(self, index, r, g, b):
    self.index = index
    self.r = r
    self.g = g
    self.b = b
    self.r_factor =random.randint(-5, 5)
    self.g_factor =random.randint(-5, 5)
    self.b_factor =random.randint(-5, 5)

  def colorPixel(self):
    if self.r_factor == 0:
      self.r_factor +=1

    if self.b_factor == 0:
      self.b_factor +=1

    if self.g_factor == 0:
      self.g_factor += 1
    
    if self.r < 30 or self.r> 50:
      self.r_factor = self.r_factor * -1

    if self.g < 30 or self.g > 240:
      self.g_factor = self.g_factor * -1
    
    if self.b < 50 or self.b > 240:
      self.b_factor = self.b_factor * -1

    self.r += self.r_factor
    self.g += self.g_factor
    self.b += self.b_factor
    pixels[self.index] = (self.r, self.g, self.b)
    time.sleep(0.03)

p0 = Pixel(0, random.randint(10, 40), random.randint(100, 240), random.randint(100, 240))
p1 = Pixel(1, random.randint(10, 40), random.randint(100, 240), random.randint(100, 240))
p2 = Pixel(2, random.randint(10, 40), random.randint(100, 240), random.randint(100, 240))
p3 = Pixel(3, random.randint(10, 40), random.randint(100, 240), random.randint(100, 240))
p4 = Pixel(4, random.randint(10, 40), random.randint(100, 240), random.randint(100, 240))
p5 = Pixel(5, random.randint(10, 40), random.randint(100, 240), random.randint(100, 240))

while True:
  p0.colorPixel()
  p1.colorPixel()
  p2.colorPixel()
  p3.colorPixel()
  p4.colorPixel()
  p5.colorPixel()

GPIO.cleanup()
