#!/usr/bin/env python3

import wazabee,sys,time

try:
	if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) == 1:
		wazabee.banner()
		print("This tool is a proof of concept of WazaBee, an attack allowing to receive and transmit 802.15.4 packets using Bluetooth Low Energy 5 chips. Two devices are currently supported: nRF52832 (Nordic SemiConductors) and CC1352-R1 (Texas Instruments).\n")
		print("Usage: "+sys.argv[0]+" [options]")
		print("\nOptions:")
		print("\t-p <port>: selects a specific serial port (default value: /dev/ttyUSB0).")
		print("\t-i: displays information about the device and the firmware version.")
		print("\t-q / --quiet: hides the banner.")
		print("\t--reset: reset the device.")
		print("\t-c <channel>/ --channel <channel>: selects a specific channel (11-26).")
		print("\t-r / --receive: enable reception mode.")
		print("\t-t <packets>/ --transmit <packets>: enable transmission mode.")
		print("\t-pcap <filename>: use a PCAP file to receive or transmit packets.")
		print("\t--check_fcs: only receives the frames including a valid FCS.")
		print("\t--calc_fcs: generates automatically the FCS of the transmitted frames.")
		print()
	else:
		if "-q" not in sys.argv and "--quiet" not in sys.argv:
			wazabee.banner()
		if "-p" in sys.argv:
			try:
				port = sys.argv[1+sys.argv.index("-p")]
			except IndexError:
				print("You have to provide a serial port.")
				sys.exit(3)
		else:
			port = "/dev/ttyUSB0"

		device = None
		try:
			device = wazabee.WazabeeDevice(port)
		except:
			print("Unable to connect to WazaBee chip.")

		if device is not None:

			if "-i" in sys.argv:
				major, minor, dev = device.getFirmwareVersion()
				print("Firmware version: WazaBee v"+str(major)+"."+str(minor))
				print("Device: "+str(dev))
				device.stop()

			if "--reset" in sys.argv:
				device.reset()
				device.stop()

			pcapFile = None
			if "--pcap" in sys.argv:
				try:
					pcapFile = sys.argv[1+sys.argv.index("--pcap")]
				except IndexError:
					print("You have to provide a PCAP file.")
					pcapFile = None

			if "-c" in sys.argv or "--channel" in sys.argv:
				try:
					try:
						channel = int(sys.argv[1+sys.argv.index("-c")])
					except ValueError:
						channel = int(sys.argv[1+sys.argv.index("--channel")])
					device.setChannel(channel)
				except (IndexError,ValueError):
					print("You have to provide a valid channel.")

			if "--check_fcs" in sys.argv:
				device.setFCSMode("valid_fcs_only")
			else:
				device.setFCSMode("all")

			if "-r" in sys.argv or "--receive" in sys.argv:
				print("(Press Ctrl+C to exit)\n")
				device.receivePackets(pcapFile)

			elif "-t" in sys.argv or "--transmit" in sys.argv:
				if pcapFile is None:
					packets = None
					try:
						try:
							packets = sys.argv[1+sys.argv.index("--transmit")].split(",")
						except ValueError:
							packets = sys.argv[1+sys.argv.index("-t")].split(",")
					except IndexError:
						print("You have to provide a list of packets.")
						packets = None
					if packets is not None:
						for p in packets:
							device.sendPacket(bytes.fromhex(p),calcFcs=("--calc_fcs" in sys.argv))
				else:
					reader = wazabee.PCAPReader(pcapFile)
					if reader.open():
						if reader.checkHeader():
							frames = reader.getFrames()
							if len(frames) > 0:
								lastTimestamp = None
								for frame in frames:
									if lastTimestamp is not None:
										time.sleep(frame[0] - lastTimestamp)
									lastTimestamp = frame[0]
									device.sendPacket(bytes([0xA7,len(frame[1])])+frame[1])
							else:
								print("The PCAP file is empty.")
							reader.close()
						else:
							print("The PCAP file is not compatible.")
					else:
						print("The PCAP file cannot be read.")

			

except KeyboardInterrupt:
	device.stop()
