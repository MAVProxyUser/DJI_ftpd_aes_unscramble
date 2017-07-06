#!/usr/bin/python
import sys
import os

from sys import platform
# Requires pycrypto - https://pypi.python.org/pypi/pycrypto
# You may want to use 'pip'. If on windows use the following instructions. 
# https://stackoverflow.com/questions/29817447/how-to-run-pip-commands-from-cmd
# You will also need Microsoft Visual C++ Compiler for Python 2.7 
# On mac, try brew, or easy_install 

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
os.environ["PATH"] = os.getcwd() + "/wget_bins" + os.pathsep + os.environ["PATH"]                 
wget = which("wget")

if not wget:
    if platform == "linux" or platform == "linux2":
        print "Linux is not supported"
    elif platform == "darwin":
        print "OSX assumes brew wget or other wget is in $PATH already"
        wget = "wget_bins/wget"
    elif platform == "win32":
        print "Windows assumes wget.exe is in %PATH% already"
        wget = "wget_bins\\wget.exe"

    if os.path.exists(wget):
        print "Using repo copy of wget"
    else:
        sys.exit( "You need wget! We can't even use the binaries we provided... something is wrong!" )

if len(sys.argv) > 1:
    if sys.argv[1] == "192.168.42.2":
        os.system("wget -m ftp://GPL:Violation@192.168.42.2/ -t 1 -T 10 -P DJI_aes_ftp_dump") # set retry to 1, because sometimes fatal.log, and others *hang*        
        print "\nCheck the contents of the folder DJI_aes_ftp_dump\n"
    elif os.path.isfile(sys.argv[1]):
        message = open(sys.argv[1], 'rb').read() 
        gplViolation = daCypha.decrypt(message)
        print gplViolation
    elif os.path.isdir(sys.argv[1]):
        print "You specified a directory... try a filename instead!?"

else:
	sys.exit( "Usage: daCypha.py <filename> (if set to 192.168.42.2 this script will mirror the DJI crafts ftpd)")



