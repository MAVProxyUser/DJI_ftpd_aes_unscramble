#!/usr/bin/python
# Swapped out the AES key with one pulled from the DJI modified Busybox ftpd.c implementation. 
#
# Find the key by running busybox ftpd inside an EABI chroot via qemu-static.  
# https://wiki.ubuntu.com/ARM/BuildEABIChroot
# aes-finder will snag it for you 
# https://github.com/mmozeiko/aes-finder
#
# $ sudo ./a.out -17898
# Searching PID 17898 ...
# [0x7f4e6c17b93c] Found AES-128 encryption key: 746869732d6165732d6b657900000000
# [0x7f4e6c17ba30] Found AES-128 decryption key: 746869732d6165732d6b657900000000
# 
# Someone needs to GPL request the changed that DJI made to busybox ;) 
# https://busybox.net/shame.html
# https://web.archive.org/web/20070101123937/http://www.busybox.net:80/shame.html

import os
import sys
import getopt
from Crypto.Cipher import AES

def decrypt_block(cipher_text):
	# Decryption
	crypto = AES.new(Key.decode("hex"), AES.MODE_CBC, IV.decode("hex"))
	plain_text = crypto.decrypt(cipher_text)
	return plain_text

def decrypt_file(cipher_filename, plain_filename, filesz):
	cipher_file = open(cipher_filename, "r")
	plain_file = open(plain_filename, "w")

	for i in xrange(0, filesz, block_sz):
		ctext = cipher_file.read(block_sz)
		ptext = decrypt_block(ctext)
		plain_file.write(ptext)

	cipher_file.close()
	plain_file.close()

def encrypt_block(plain_text):
	# Encryption
	crypto = AES.new(Key.decode("hex"), AES.MODE_CBC, IV.decode("hex"))
	cipher_text = crypto.encrypt(plain_text)
	return cipher_text

def encrypt_file(plain_filename, cipher_filename,filesz):
	plain_file = open(plain_filename, "r")
	cipher_file = open(cipher_filename, "w")

	for i in xrange(0, filesz, block_sz):
		ptext = plain_file.read(block_sz)
		ctext = encrypt_block(ptext)
		cipher_file.write(ctext)

	cipher_file.close()
	plain_file.close()


def main(argv):
   do_encrypt = False
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"dehi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'djicrypt.py d/e -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-d':
      	print "Decrypting..."
      	do_encrypt = False
      elif opt == '-e':
      	print "Encrypting..."
      	do_encrypt = True
      elif opt == '-h':
      	print 'djicrypt.py d/e -i <inputfile> -o <outputfile>'
        sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inputfile
   print 'Output file is "', outputfile

   filesz = os.path.getsize(inputfile)

   if do_encrypt == False:
   	decrypt_file(inputfile, outputfile, filesz)
   else:
   	encrypt_file(inputfile, outputfile, filesz)
   
block_sz = 256
#cipher_filename = "UnitA.bin"
#plain_filename = "UnitA.dec"
#Key = "7F0B9A5026674ADA0BB64F27E6D8C8A6"
Key = "746869732d6165732d6b657900000000"
IV = "00000000000000000000000000000000"

if __name__ == "__main__":
   main(sys.argv[1:])




