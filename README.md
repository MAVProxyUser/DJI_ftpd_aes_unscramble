# DJI_ftpd_aes_unscramble
DJI has modified the GPL Busybox ftpd on Mavic, Spark, &amp; Inspire 2 to include scrambling of downloaded files... 

I miss the good ole days of public tar & feathering over GPL violations!

```
"The following products and/or projects appear to use BusyBox, but do not appear to release source code as required by the BusyBox license. This is a violation of the law! The distributors of these products are invited to contact Erik Andersen if they have any confusion as to what is needed to bring their products into compliance, or if they have already brought their product into compliance and wish to be removed from the Hall of Shame."
```

```
This page is no longer updated, these days, BusyBox handles enforcement of our license via our fiscal sponsor, Software Freedom Conservancy instead. Please email <gpl@busybox.net> if you believe you've found a violation of BusyBox's license, the GPLv2.

Previously, this page listed products that included BusyBox but included neither source code nor offer for one. The BusyBox project has decided to not publicly shame companies until Conservancy has an opportunity to talk privately with companies who violate the GPL to convince them to comply with BusyBox's license.
```

https://web-beta.archive.org/web/20130116093247/http://busybox.net/shame.html

In an attempt to obfuscate the files downloaded from several DJI products, an AES function was added to the ftpd download routines of busybox. 

It is extremely trivial to extract the binary using binwalk from one of the available firmware downloads. From here it can be Reverse Engineered.


On OSX you can navigate to: /Applications/Assistant_1_1_0.app/Contents/MacOS/Data/firm_cache 
On Windows to: C:\Program Files (x86)\DJI Product\DJI Assistant 2\ Assistant\Data\firm_cache

Run binwalk with the extraction flag against any appropriate firmware file. 
```
$ grep busybox wm* -r
Binary file wm220_0100_v02.05.04.34_20170209_ca02.pro.fw.sig matches
Binary file wm220_0100_v02.06.04.84_20170324_ca02.pro.fw.sig matches
Binary file wm220_0801_v01.04.17.03_20170120.pro.fw.sig matches
Binary file wm220_0801_v01.05.00.20_20170331.pro.fw.sig matches
Binary file wm220_0805_v01.01.00.71_20161227.pro.fw.sig matches
Binary file wm220_0805_v01.01.00.87_20170427.pro.fw.sig matches
Binary file wm220_1301_v01.04.17.03_20170120.pro.fw.sig matches
Binary file wm220_1301_v01.05.00.23_20170418.pro.fw.sig matches
Binary file wm220_2801_v01.02.21.01_20170421.pro.fw.sig matches
```

Pick one... just make sure it doesn't contain busybox for the Ambarella SoC (contained within the squashfs)
```
$ binwalk -e wm220_0801_v01.04.17.03_20170120.pro.fw.sig
```
Launch the binary in a chroot via qemu-user-static. 
https://wiki.ubuntu.com/ARM/BuildEABIChroot

```
# ./busybox tcpsvd -vE 0.0.0.0 21 ./busybox ftpd -wv /tmp/
tcpsvd: listening on 0.0.0.0:21, starting
tcpsvd: status 1/30
tcpsvd: start 9062 127.0.0.1:21-127.0.0.1:39922
```

Download, compile, and run aes-finder against the ftp binary. Extract the AES key by running against the PID. 
https://github.com/mmozeiko/aes-finder

```
$ sudo ./a.out -9062
Searching PID 9062 ...
[0x7f4e6c17b93c] Found AES-128 encryption key: 746869732d6165732d6b657900000000
[0x7f4e6c17ba30] Found AES-128 decryption key: 746869732d6165732d6b657900000000

$ echo -e "\x74\x68\x69\x73\x2d\x61\x65\x73\x2d\x6b\x65\x79\x00\x00\x00\x00"
this-aes-key
```

This oddly enough was the string that made me look for the routine in the first place. It shows up in clear text in the binary. 
Busybox does not normally have an AES function, so this was immediately a red flag. 

I had a hunch that DJI reused their encryption choices... and they did, the same routines used on the NAZA firmware work on the downloads. 

https://hackaday.io/project/19995-hacking-dji-naza-m/log/53751-big-dump
https://cdn.hackaday.io/files/19995855466080/Toolss.7z

Simply replace the AES key with the one above in the tool provided by seasonalvegetables3. 

```
#Key = "7F0B9A5026674ADA0BB64F27E6D8C8A6"
Key = "746869732d6165732d6b657900000000"
IV = "00000000000000000000000000000000"
```

This project will recurvively download the contents of the ftp server, and decrypt them for you in a local plaintext mirror. 

In essence using code in this repo would be the same as running: 
```
$ wget -m ftp://GPL:Violation@192.168.42.2/
```

Followed by:
```
python djicrypt.py -d -i downloadedfile -o outputfile
```


