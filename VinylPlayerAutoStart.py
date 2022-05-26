#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 2)
reader = SimpleMFRC522()

emptyCount = 0
previousRead = "nix"

try:
	while True:
		print("EPMTYCOUNT: ", emptyCount)
		print("Ready for some tunes!")
		pixels.fill((40,0,80))
		id, text = reader.read_no_block()

		if emptyCount > 3:
			print("pause Music")
			stopR = requests.get("http://192.168.2.149:5005/pauseAll")
			emptyCount = 0
			previousRead = "nix"

		time.sleep(1)
		if (text == None):
			emptyCount += 1
		else:
			emptyCount = 0
			if (previousRead != text and text.strip().find("spotify") != -1):
				getRequest = "http://192.168.2.149:5005/Foyer/spotify/now/" + text.strip()
				r = requests.get(getRequest)
				previousRead = text
				pixels.fill((0, 200, 0))
				time.sleep(0.2)
				pixels.fill((0, 0, 0))
				time.sleep(0.2)
			elif (text.strip().find("spotify") != -1 and text != None):
				print("weiter wie gehabt")
			else:
				print("Invalid URI", text)
				pixels.fill((200, 0, 0))
				time.sleep(0.2)
				pixels.fill((0, 0, 0))
				time.sleep(0.2)

except KeyboardInterrupt:
	GPIO.cleanup()
	raise
