import time
import nfc
import requests
import uuid
import appsettings #you shouldnt need to edit this file
import usersettings #this is the file you might need to edit
import sys
import board
import RPi.GPIO as GPIO
import neopixel
import random
from threading import Thread
import threading

pixels = neopixel.NeoPixel(board.D18, 6)
run_aurora_animation = False
start_shutdown_sequence = False

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

p0 = Pixel(0, random.randint(100, 240), random.randint(100, 240))
p1 = Pixel(1, random.randint(100, 240), random.randint(100, 240))
p2 = Pixel(2, random.randint(100, 240), random.randint(100, 240))
p3 = Pixel(3, random.randint(100, 240), random.randint(100, 240))
p4 = Pixel(4, random.randint(100, 240), random.randint(100, 240))
p5 = Pixel(5, random.randint(100, 240), random.randint(100, 240))

def released(tag):
	global run_aurora_animation
	global start_shutdown_sequence
	print("Pause Music")
	run_aurora_animation = False
	stop_r = requests.get(usersettings.sonoshttpaddress + "/pauseAll")

# this function gets called when a NFC tag is detected
def touched(tag):
	global start_shutdown_sequence
	global run_aurora_animation
	global sonosroom_local
	print('Say hello', tag)

	if tag.ndef:
		print(tag.ndef)
		for record in tag.ndef.records:
			try:
				print(record.text)
				receivedtext = record.text
			except:
				print("Error reading a *TEXT* tag from NFC.")
				return True
			
			receivedtext_lower = receivedtext.lower()

			print("")
			print("Read from NFC tag: "+ receivedtext)

			servicetype = ""

			if receivedtext == "shutdown":
				start_shutdown_sequence = True
				pixels.fill((255, 0, 0))
				time.sleep(1);
				pixels.fill((0, 0, 0))
				time.sleep(1);
				pixels.fill((255, 0, 0))
				time.sleep(1);
				pixels.fill((0, 0, 0))
				time.sleep(1);
				pixels.fill((255, 0, 0))
				time.sleep(1);
				pixels.fill((0, 0, 0))
				print ("Pi will be shut down")
				os.system("sudo shutdown now -h")
				return True

				
			if receivedtext == "reboot":
				start_shutdown_sequence = True
				pixels.fill((0, 255, 0))
				time.sleep(1);
				pixels.fill((0, 0, 0))
				time.sleep(1);
				pixels.fill((0, 255, 0))
				time.sleep(1);
				pixels.fill((0, 0, 0))
				time.sleep(1);
				pixels.fill((0, 255, 0))
				time.sleep(1);
				pixels.fill((0, 0, 0))
				print ("Pi will be rebooted")
				os.system("sudo reboot")
				return True
			
			#check if a full HTTP URL read from NFC
			if receivedtext_lower.startswith ('http'):
				servicetype = "completeurl"
				sonosinstruction = receivedtext

			#determine which music service read from NFC
			if receivedtext_lower.startswith ('spotify'):
				servicetype = "spotify"
				sonosinstruction = "spotify/now/" + receivedtext

			if receivedtext_lower.startswith ('tunein'):
				servicetype = "tunein"
				sonosinstruction = receivedtext
			
			if receivedtext_lower.startswith ('favorite'):
				servicetype = "favorite"
				sonosinstruction = receivedtext
			
			if receivedtext_lower.startswith ('amazonmusic:'):
				servicetype = "amazonmusic"
				sonosinstruction = "amazonmusic/now/" + receivedtext[12:]

			if receivedtext_lower.startswith ('apple:'):
				servicetype = "applemusic"
				sonosinstruction = "applemusic/now/" + receivedtext[6:]

			if receivedtext_lower.startswith ('applemusic:'):
				servicetype = "applemusic"
				sonosinstruction = "applemusic/now/" + receivedtext[11:]

			if receivedtext_lower.startswith ('bbcsounds:'):
				servicetype = "bbcsounds"
				sonosinstruction = 'bbcsounds/play/' + receivedtext[10:]

			#check if a Sonos "command" or room change read from NFC
			if receivedtext_lower.startswith ('command'):
				servicetype = "command"
				sonosinstruction = receivedtext[8:]
			
			if receivedtext_lower.startswith ('room'):
				servicetype = "room"
				sonosroom_local = receivedtext[5:]
				print ("Sonos room changed to " + sonosroom_local)
				return True

			#if no service or command detected, exit
			if servicetype == "":
				print ("Service type not recognised. NFC tag text should begin spotify, tunein, amazonmusic, apple/applemusic, command or room.")
				return True
			
			print ("Detected " + servicetype + " service request")

			#build the URL we want to request
			if servicetype.lower() == 'completeurl':
				urltoget = sonosinstruction
			else:
				urltoget = usersettings.sonoshttpaddress + "/" + sonosroom_local + "/" + sonosinstruction
			
			#check Sonos API is responding
			try:
				r = requests.get(usersettings.sonoshttpaddress)
			except:
				print ("Failed to connect to Sonos API at " + usersettings.sonoshttpaddress)
				return True

			#clear the queue for every service request type except commands
			if servicetype != "command":
				print ("Clearing Sonos queue")
				r = requests.get(usersettings.sonoshttpaddress + "/" + sonosroom_local + "/clearqueue")

			#use the request function to get the URL built previously, triggering the sonos
			print ("Fetching URL via HTTP: "+ urltoget)
			r = requests.get(urltoget)

			if r.status_code != 200:
				print ("Error code returned from Sonos API")
				return True
			
			print ("Sonos API reports " + r.json()['status'])
			run_aurora_animation = True

	else:
		print("")
		print ("NFC reader could not read tag. This can be because the reader didn't get a clear read of the card. If the issue persists then this is usually because (a) the tag is encoded (b) you are trying to use a mifare classic card, which is not supported or (c) you have tried to add data to the card which is not in text format. Please check the data on the card using NFC Tools on Windows or Mac.")

	return True

print("")
print("")
print("Loading and checking readnfc")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("")
print("SCRIPT")
print ("You are running version " + appsettings.appversion + "...")

print("")
print("NFC READER")
print("Connecting to NFC reader...")
try:
	reader = nfc.ContactlessFrontend(usersettings.nfc_reader_path)
except IOError as e:
	print ("... could not connect to reader")
	print ("")
	print ("You should check that the reader is working by running the following command at the command line:")
	print (">  python -m nfcpy")
	print ("")
	print ("If this reports that the reader is in use by readnfc or otherwise crashes out then make sure that you don't already have readnfc running in the background via pm2. You can do this by running:")
	print (">  pm2 status             (this will show you whether it is running)")
	print (">  pm2 stop readnfc       (this will allow you to stop it so you can run the script manually)")
	print ("")
	print ("If you want to remove readnfc from running at startup then you can do it with:")
	print (">  pm2 delete readnfc")
	print (">  pm2 save")
	print (">  sudo reboot")
	print ("")
	sys.exit()

print("... and connected to " + str(reader))

print ("")
print ("SONOS API")
sonosroom_local = usersettings.sonosroom
print ("API address set to " + usersettings.sonoshttpaddress)
print ("Sonos room set to " + sonosroom_local)

print ("Trying to connect to API ...")
try:
	r = requests.get(usersettings.sonoshttpaddress)
except:
	print ("... but API did not respond. This could be a temporary error so I won't quit, but carry on to see if it fixes itself")

if r.status_code == 200:
	print ("... and API responding")


pixels.fill((255, 204, 25))
print("")
print("OK, all ready! Present an NFC tag.")
print("")

def update_aurora():
	global run_aurora_animation
	global start_shutdown_sequence

	while True:
		if not start_shutdown_sequence:
			if run_aurora_animation:
				p0.colorPixel()
				p1.colorPixel()
				p2.colorPixel()
				p3.colorPixel()
				p4.colorPixel()
				p5.colorPixel()
				time.sleep(0.01)
			
			else:
				pixels.fill((255, 204, 25))

thread_aurora = Thread(target=update_aurora)

while True:
	try:
		
		if not thread_aurora.is_alive():
			thread_aurora.start()
	
		reader.connect(rdwr={'on-connect': touched, 'on-release': released ,'beep-on-connect': False})
		time.sleep(0.1);
	
	except KeyboardInterrupt:
		pixels.fill((0, 0, 0))
		GPIO.cleanup()
		raise

