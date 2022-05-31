#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 6)

while True:
	print("Ready for some tunes!")
	pixels.fill((0,200, 150))
	time.sleep(0.3)
	pixels.fill((200, 200, 200))
	time.sleep(0.3)

GPIO.cleanup()
