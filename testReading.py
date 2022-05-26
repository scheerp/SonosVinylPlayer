#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 2)
reader = SimpleMFRC522()

failCounter = 0
successCounter = "nix"

while True:
	GPIO.cleanup()
	readingSuccess = False
	id, text = reader.read()
	print("start reading")
	pixels.fill((40,0,80))
	time.sleep(10)
	print(text)
	