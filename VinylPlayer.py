#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests

reader = SimpleMFRC522()

try:
        id, text = reader.read()

        getRequest = "http://192.168.2.149:5005/Foyer/spotify/now/" + text.strip()

        r = requests.get(getRequest)

finally:
        GPIO.cleanup()
