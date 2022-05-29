#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time
import board
import neopixel
import random

pixels = neopixel.NeoPixel(board.D18, 6)
reader = SimpleMFRC522()

countIsActive = False
emptyCount = 0
previousRead = "nix"
pixels.fill((255, 204, 25))

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
		print("update!", self.g, self.b)
		pixels[self.index] = (0, self.g, self.b)
		time.sleep(0.001)

p0 = Pixel(0, random.randint(100, 240), random.randint(100, 240))
p1 = Pixel(1, random.randint(100, 240), random.randint(100, 240))
p2 = Pixel(2, random.randint(100, 240), random.randint(100, 240))
p3 = Pixel(3, random.randint(100, 240), random.randint(100, 240))
p4 = Pixel(4, random.randint(100, 240), random.randint(100, 240))
p5 = Pixel(5, random.randint(100, 240), random.randint(100, 240))

try:
	while True:
		# print("Ready for some tunes!")
		id, text = reader.read_no_block()
		# print("emptyCount", emptyCount)
		# print("text", text)
		# print("countIsActive", countIsActive)

		if countIsActive:
			if emptyCount > 3:
				print("pause Music")
				stopR = requests.get("http://192.168.2.149:5005/pauseAll")
				emptyCount = 0
				previousRead = "nix"
				pixels.fill((255, 204, 25))
				countIsActive = False

			#time.sleep(0.05)
			if (text == None):
				emptyCount += 1

		if text != None:
			if (previousRead != text and text.strip().find("spotify") != -1):
				print("play Music")
				getRequest = "http://192.168.2.149:5005/Wohnzimmer/spotify/now/" + text.strip()
				r = requests.get(getRequest)
				previousRead = text
				emptyCount = 0
				countIsActive = True
			elif (text.strip().find("spotify") != -1):
				print("weiter wie gehabt")

				for x in range(30):
					p0.colorPixel()
					p1.colorPixel()
					p2.colorPixel()
					p3.colorPixel()
					p4.colorPixel()
					p5.colorPixel()
				emptyCount = 0
				#pixels.fill((0, 200, 180))
			else:
				print("Invalid URI", text)
				pixels.fill((200, 0, 0))
				time.sleep(0.2)
				pixels.fill((0, 0, 0))
				emptyCount = 0

except KeyboardInterrupt:
	pixels.fill((0, 0, 0))
	GPIO.cleanup()
	raise
