#!/usr/bin/python
import sys
from Crypto.Cipher import AES
key = "\x74\x68\x69\x73\x2d\x61\x65\x73\x2d\x6b\x65\x79\x00\x00\x00\x00"
iv  = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
daCypha = AES.new(key, AES.MODE_CBC, iv)
message = ""
if len(sys.argv) > 1:
	message = open(sys.argv[1], 'r').read()
else:
	print "Usage: daCypha.py <filename>"
gplViolation = daCypha.decrypt(message)
print gplViolation


