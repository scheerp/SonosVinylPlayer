#!/usr/bin/env python
# -*- coding: latin-1 -*-

import os
import sys
sys.path.insert(1, os.path.split(sys.path[0])[0])

import nfc
import nfc.clf
import nfc.tag

def connected(tag): print(tag.ndef.message.pretty() if tag.ndef else "Sorry, no NDEF"); return False
clf = nfc.ContactlessFrontend('usb')
tag = clf.connect(rdwr={'on-connect': connected})

clf.close()
