# DJI_ftpd_aes_unscramble

Update: DJI has complied with the GPL requests for the code related to this repo:
http://www.dji.com/opensource
https://s3.amazonaws.com/dji-brandsite-document/opensource/busybox-1.25.1.tar.gz

DJI has modified the GPL Busybox ftpd on Mavic, Spark, &amp; Inspire 2 to include scrambling of downloaded files... 

Windows executable release created via:
```
c:\python27\Scripts\pyinstaller.exe --add-data=wget_bins;wget_bins dji_ftpd_descrambler.py
```
If not using packaged release for Windows, make sure you have pip, and that pycrypto is installed

Usage:
Make sure you have a DJI Mavic, Inspire 2, or Phantom 4, or Spark connected. 

Mirror the FTPD via the script, OR manually pull down a target file. 
```
$ python dji_ftpd_descrambler.py 192.168.42.2
--2017-05-25 23:57:13--  ftp://GPL:*password*@192.168.42.2/
           => ‘DJI_aes_ftp_dump/192.168.42.2/.listing’
Connecting to 192.168.42.2:21... ^C
Check the contents of the folder DJI_aes_ftp_dump
...

Verify the file is AES encrytped aka "scrambled" per some forum chatter. 
$ xxd DJI_aes_ftp_dump/192.168.42.2/upgrade/dji/log/cp_assert.log  | head -n 10
00000000: dee9 a171 7fad 24e2 a2ad fe52 f2a9 43e4  ...q..$....R..C.
00000010: cdf3 ab35 4ec3 82a8 f491 f3e5 40a8 c92c  ...5N.......@..,
00000020: b80a 8c8e 0bef 6bf5 5505 b71c d819 9bde  ......k.U.......
00000030: cf23 f181 68b1 ae23 6305 1c8b 4d1a 986c  .#..h..#c...M..l
00000040: 4d3e 569a 97e1 33b0 7a05 4ff1 92c2 d88d  M>V...3.z.O.....
00000050: 20b7 d872 5ef4 a288 f25d dc06 a8e7 6b0d   ..r^....]....k.
00000060: dc14 85c1 45eb bc59 36d8 1c63 b17f d35b  ....E..Y6..c...[
00000070: 07c0 1499 ff5b 4c0f 7cc7 df67 d09b a2ea  .....[L.|..g....
00000080: 0dfc fcb3 8aab 5f06 aace 0f41 a6c6 fb89  ......_....A....
00000090: 5d13 a609 c74a 7318 4734 2d95 d5bc b975  ]....Js.G4-....u
```

Descramble the file... profit! 
```
$ python dji_ftpd_descrambler.py DJI_aes_ftp_dump/192.168.42.2/upgrade/dji/log/cp_assert.log  | head -n 10
    PBS^U\5] [0x0] state=0, reset phy
[1980/00/01 0:0:5] [0x0]========= machine=1, state=0, runtime=72 =========
[1980/00/01 0:0:5] [0x0] state=0, [0] reset mac to idle
[1980/00/01 0:0:7] [0x1866] state=0, recv shakehand req
[1980/00/01 0:0:7] [0x187c] state from 0 to connect
[2017/04/14 14:42:30] [0x3d27d0] state=3, connect to out_of_sync
[2017/04/14 14:42:30] [0x3d27d0] state=3, [1] reset mac to idle
[2017/04/14 14:44:8] [0x47d] state=3, recv shakehand req
[2017/04/14 14:44:8] [0x4c3] state=3, recv shakehand req
[2017/04/14 14:44:8] [0x530] state from 3 to connect
```
On Windows the process works the same, with alternate synatx on the command line. 

You can use the new bash interface:
```
MavproxyUser@DESKTOP-QPUF664 MINGW64 ~/Desktop/DJI_ftpd_aes_unscramble (master)
$ python dji_ftpd_descrambler.py kernel00.log
oOZTPTP7] c0 1 (init) init: untracked pid 621 exited
<7>[   52.603083] c3 0 (swapper/3) Warnning: timer5 int-excep
<7>[   77.938720] c0 419 (dji_hdvt_gnd) bridge: start_xmit info: lmi42 xmit skb cb444000 CP busy!
<7>[   78.001593] c0 461 (keyscan_task) bridge: start_xmit info: lmi42 xmit skb cb444000 CP ready!
<7>[  162.814198] c3 439 (dji_hdvt_gnd) bridge: start_xmit info: lmi42 xmit skb ce24a300 CP busy!
<7>[  162.891897] c0 273 (MB_Socket_Recei) bridge: start_xmit info: lmi42 xmit skb ce24a300 CP ready!
<7>[  356.750230] c0 419 (dji_hdvt_gnd) bridge: start_xmit info: lmi42 xmit skb ce39fa80 CP busy!
<7>[  356.814311] c0 461 (keyscan_task) bridge: start_xmit info: lmi42 xmit skb ce39fa80 CP ready!
```
Or make use of the standard cmd.exe interface:
```
C:\Users\MavproxyUser\Desktop\DJI_ftpd_aes_unscramble>python dji_ftpd_descrambler.py kernel00.log | more
!!!New kernel log start!!!

<6>[    0.000000] c0 0 (swapper) Booting Linux on physical CPU 0x100
<6>[    0.000000] c0 0 (swapper) Initializing cgroup subsys cpu
<6>[    0.000000] c0 0 (swapper) Initializing cgroup subsys cpuacct
<5>[    0.000000] c0 0 (swapper) Linux version 3.10.62 (jenkins@APServer01) (gcc version 4.7 (GCC) ) #1 SMP PREEMPT Mon Feb 27 20:12:56 CST 2017
<4>[    0.000000] c0 0 (swapper) CPU: ARMv7 Processor [410fc075] revision 5 (ARMv7), cr=10c5387d
<4>[    0.000000] c0 0 (swapper) CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
<4>[    0.000000] c0 0 (swapper) Machine: Leadcore Innopower
<4>[    0.000000] c0 0 (swapper) start comip_parse_tag_mem_ext.
<4>[    0.000000] c0 0 (swapper) Physical memory layout:
<4>[    0.000000] c0 0 (swapper)     DRAM Bank1  : 0x00000000 - 0x20000000  ( 512 MB)
<4>[    0.000000] c0 0 (swapper)     Modem       : 0x00000000 - 0x06400000  ( 100 MB)
<4>[    0.000000] c0 0 (swapper)     Kernel Bank1: 0x06400000 - 0x16800000  ( 260 MB)
<4>[    0.000000] c0 0 (swapper)     Framebuffer : 0x16800000 - 0x17800000  (  16 MB)
-- More  --
```
Alternatively on windows you can use the precompied .exe (see the Releases tab)
```
C:\Users\kfinisterre\Desktop\dji_ftpd_descrambler>dji_ftpd_descrambler.exe c:\Users\kfinisterre\Desktop\kernel01.log | more
h
VTVSPW] c1 11916 (kworker/u10:0) bridge: drop 0xd228 packet due to buffer full
<7>[ 1380.255734] c1 11916 (kworker/u10:0) bridge: drop 0xd28c packet due to buffer full
<7>[ 1382.825736] c0 26031 (kworker/u10:1) bridge: drop 0xd2f0 packet due to buffer full
```

Description:


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

Alternately you can just use openssl:
```
openssl enc -d -nosalt -in downloadedfile -aes-128-cbc -K 746869732d6165732d6b657900000000 -iv 00000000000000000000000000000000
```

And of course *our* script as detailed above in Usage:

In this example the ever so valuable DAAK is extracted... as is the WAEK (wireless password)

$ python dji_ftpd_descrambler.py  /tmp/192.168.42.2_drone/upgrade/dji/log/kernel01.log  | grep daak | head -n 1
```
<5>[    0.000000] c0 0 (swapper) Kernel command line: watchdog_thresh=3 console=ttyS1,921600 vmalloc=412M android firmware_class.path=/vendor/firmware isolcpus=2,3,4 
initrd=0x07400000,1M lcpart=mmcblk0=gpt:0:2000:200,ddr:2000:2000:200,env:4000:2000:200,panic:6000:2000:200,amt:8000:20000:200,factory:28000:4000:200,factory_out:2c000:4000:200,
recovery:30000:8000:200,normal:38000:8000:200,system:40000:40000:200,vendor:80000:20000:200,cache:a0000:80000:200,blackbox:120000:400000:200,userdata:520000:228000:200  
chip_sn=31337000 board_sn=01EAT2D111XXXX daak=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA daek=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA drak=6f707f2962351d75bc089ac34da119fa 
saak=6f402fb8625205ce9bdd580217d218d8 waek=WIFIPASS production quiet board_id=0xe2200026
```
