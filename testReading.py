#!/usr/bin/env python

#import RPi.GPIO as GPIO
#from mfrc522 import SimpleMFRC522
#import requests
#import time
#import board
#import neopixel
#
#pixels = neopixel.NeoPixel(board.D18, 2)
#reader = SimpleMFRC522()
#
#failCounter = 0
#successCounter = "nix"
#
#while failCounter < 4:
#	GPIO.cleanup()
#	time.sleep(10)
#	id, text = reader.read()
#	print("start reading")
#	pixels.fill((40,0,80))
#	print(text)
#	if (text.find("spotify") != 1):
#		failCounter +=1
#		print("failed ++", failCounter)
	
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
emptyCount = 0

try:
	while emptyCount < 4:
		print("Hold a tag near the reader")
		print(emptyCount)
		id, text = reader.read()
		print(reader.read())
		print("ID: %s\nText: %s" % (id,text))
		sleep(5)
		emptyCount += 1
except KeyboardInterrupt:
	GPIO.cleanup()
	raise
