# Presentation

WazaBee is an attack allowing to transmit and receive 802.15.4 packets by diverting Bluetooth Low Energy chips. This software is a basic proof of concept (PoC) implementing the two communication primitives used by this attack. This source code is not dedicated to an offensive usage, and it is only provided for research purposes. It is released as an open-source project under MIT license.

This repository contains the Command Line Interface allowing to interact with a board embedding WazaBee PoC. It requires to build and flash the WazaBee PoC firmware. Two development boards are currently supported:

* **Adafruit nRF52832 Feather** (*nRF52832* from Nordic Semiconductors)
* **Texas Instruments CC1352-R1** (*CC1352-R1* from Texas Instruments)

# Installation

* Install scapy:
```
$ sudo pip3 install scapy
```

* Plug the board embedding Wazabee and execute wazabee_cli:
```
$ ./wazabee_cli.py -i
```

Usage
=====

* First of all, check if you can communicate with the board using the **-i** option:
```
$ ./wazabee_cli.py -i
```

It should produce an output similar to the following one:
```
_ _ _ ____ ___  ____ ___  ____ ____ 
| | | |__|   /  |__| |__] |___ |___ 
|_|_| |  |  /__ |  | |__] |___ |___ 
                            
Firmware version: WazaBee v1.0
Device: NRF52832
```

If needed, provide the serial port to use thanks to the **-p** option:
```
$ ./wazabee_cli.py -p /dev/ttyACM0 -i
```

* You can receive 802.15.4 frames using **-r** option, and choose a specific channel between 11 and 26 using **-c**:
```
$ ./wazabee_cli.py -c 12 -r
_ _ _ ____ ___  ____ ___  ____ ____ 
| | | |__|   /  |__| |__] |___ |___ 
|_|_| |  |  /__ |  | |__] |___ |___ 
                            
(Press Ctrl+C to exit)

1591111115.2063422: a7 12 61 88 f9 32 33 00 00 00 00 d3 00 68 65 6c 6c 6f 9e e0 (FCS: OK)
1591111115.5315676: a7 12 61 88 f9 32 33 00 00 00 00 d3 00 68 65 6c 6c 6f 9e e0 (FCS: OK)
1591111116.4340115: a7 12 61 88 fa 32 33 00 00 00 00 d4 00 68 65 6c 6c 6f b8 a4 (FCS: OK)
1591111117.4339259: a7 12 61 88 fb 32 33 00 00 00 00 d5 00 68 65 6c 6c 6f 87 45 (FCS: OK)
1591111118.4344916: a7 12 61 88 fc 32 33 00 00 00 00 d6 00 68 65 6c 6c 6f 6e 9d (FCS: OK)
1591111119.4359083: a7 12 61 88 fd 32 33 00 00 00 00 d7 00 68 65 6c 6c 6f 51 7c (FCS: OK)
1591111120.4362369: a7 12 61 88 fe 32 33 00 00 00 00 d8 00 68 65 6c 6c 6f 9b e6 (FCS: OK)

```

If you want to export the received frames in a PCAP file, use the **--pcap** option to provide a filename: 
```
./wazabee_cli.py -c 12 -r --pcap test.pcap
```

You can also enable the **--check_fcs** option if you want only display frames including a valid FCS.

* You can transmit 802.15.4 frames using **-t** option:
```
$ ./wazabee_cli.py -c 12 -t a7126188f9323300000000d30068656c6c6f9ee0,a7126188fd323300000000d70068656c6c6f517c
_ _ _ ____ ___  ____ ___  ____ ____ 
| | | |__|   /  |__| |__] |___ |___ 
|_|_| |  |  /__ |  | |__] |___ |___ 
                            
Transmitting: a7 12 61 88 f9 32 33 00 00 00 00 d3 00 68 65 6c 6c 6f 9e e0 (FCS:e0 9e)
Transmitting: a7 12 61 88 fd 32 33 00 00 00 00 d7 00 68 65 6c 6c 6f 51 7c (FCS:7c 51)
```

If you want to transmit the frames included in a PCAP file, use the **--pcap** option to provide a filename:
```
$ ./wazabee_cli.py -c 12 -t --pcap test.pcap
_ _ _ ____ ___  ____ ___  ____ ____ 
| | | |__|   /  |__| |__] |___ |___ 
|_|_| |  |  /__ |  | |__] |___ |___ 
                            
Transmitting: a7 12 61 88 35 32 33 00 00 00 00 10 00 68 65 6c 6c 6f 80 d0 (FCS:d0 80)
Transmitting: a7 12 61 88 35 32 33 00 00 00 00 10 00 68 65 6c 6c 6f 80 d0 (FCS:d0 80)
Transmitting: a7 12 61 88 36 32 33 00 00 00 00 11 00 68 65 6c 6c 6f 6b cc (FCS:cc 6b)
Transmitting: a7 12 61 88 37 32 33 00 00 00 00 12 00 68 65 6c 6c 6f ef 1a (FCS:1a ef)
Transmitting: a7 12 61 88 38 32 33 00 00 00 00 13 00 68 65 6c 6c 6f de 1a (FCS:1a de)
Transmitting: a7 12 61 88 39 32 33 00 00 00 00 14 00 68 65 6c 6c 6f 2c a3 (FCS:a3 2c)
Transmitting: a7 12 61 88 3a 32 33 00 00 00 00 15 00 68 65 6c 6c 6f c7 bf (FCS:bf c7)
```

You can also use the **--calc_fcs** option in order to automatically calculate the FCS:
```
$ ./wazabee_cli.py -c 12 -t a7126188f9323300000000d30068656c6c6f,a7126188fd323300000000d70068656c6c6f --calc_fcs
```

