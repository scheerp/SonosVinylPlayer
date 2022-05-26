#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 2)
reader = SimpleMFRC522()

try:
        print("Ready for some tunes!")
        pixels.fill((40,0,80))

        id, text = reader.read()

        getRequest = "http://192.168.2.149:5005/Foyer/spotify/now/" + text.strip()
        
        r = requests.get(getRequest)
        pixels.fill((0, 200, 0))
        time.sleep(0.2)
        pixels.fill((0, 0, 0))
        time.sleep(0.2)
        pixels.fill((0, 200, 0))
        time.sleep(0.2)
        pixels.fill((0, 0, 0))
        time.sleep(0.2)
        pixels.fill((0, 200, 0))
        time.sleep(0.2)
finally:
        pixels.fill((0, 0, 0))
        GPIO.cleanup()
