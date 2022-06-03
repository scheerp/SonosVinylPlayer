import nfc
with nfc.ContactlessFrontend('udp') as clf:
	print(clf)
