#!/usr/bin/python
import sys
import os
from sys import platform
from Crypto.Cipher import AES

def which(program):
    import os
    def is_exe(fpath):
       return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


key = "\x74\x68\x69\x73\x2d\x61\x65\x73\x2d\x6b\x65\x79\x00\x00\x00\x00"
iv  = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
daCypha = AES.new(key, AES.MODE_CBC, iv)
message = ""
wget = which("wget")

if not wget:
    if platform == "linux" or platform == "linux2":
        print "Linux is not supported"
    elif platform == "darwin":
        print "OSX assumes brew wget or other wget is in $PATH already"
    elif platform == "win32":
        print "Windows assumes wget.exe is in %PATH% already"

    os.environ["PATH"] += os.pathsep + os.getcwd() + "/wget_bins"

    wget = which("wget")

    if not wget:
        sys.exit( "You need wget! We can't even use the binaries we provides... something is wrong!" )

if len(sys.argv) > 1:
	message = open(sys.argv[1], 'r').read()
else:
	system.exit( "Usage: daCypha.py <filename>")

gplViolation = daCypha.decrypt(message)
print gplViolation


