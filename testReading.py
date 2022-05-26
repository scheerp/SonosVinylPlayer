#!/usr/bin/env python
	
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
emptyCount = 0

try:
	while emptyCount < 4:
		print("Hold a tag near the reader")
		print(emptyCount)
		id, text = reader.read_no_block()
		print("ID: %s\nText: %s" % (id,text))
		sleep(5)
		if (text == None):
			emptyCount += 1
		else:
			emptyCount = 0
except KeyboardInterrupt:
	GPIO.cleanup()
	raise
