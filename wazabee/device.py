import time
from serial import Serial
from serial.serialutil import SerialException
from queue import Queue
from sys import exit
from threading import Thread
from .layers import *
from .pcap import PCAPWriter

class WazabeeDevice:
	def __init__(self,port="/dev/ttyUSB0"):
		self.port = port
		self.ready = False
		self.initSerialComm()
		self.frameQueue = Queue()
		self.commandQueue = Queue()
		self.enableRxThread()

	def _rxThread(self):
		try:
			inFrame = False
			while self.rxThreadEnabled:
				next = self.serialComm.read(1)
				if inFrame:
					recvBuffer += next
					if len(recvBuffer) > 3:
						if (
						(recvBuffer[2] == 0x01 and ((recvBuffer[3] == 0x00 and len(recvBuffer[4:]) == 3) or
						(recvBuffer[3] in (0x01,0x02,0x03,0x04) and len(recvBuffer[4:]) == 1) or
						(recvBuffer[3] in (0x05,0x06)))) or 
						(recvBuffer[2] == 0x02 and recvBuffer[3]+1 == len(recvBuffer[4:]))
						): 
							packet = Wazabee_Hdr(recvBuffer)
							if packet.type == 0x02:
								self.frameQueue.put(packet)
							else:
								self.commandQueue.put(packet)
							inFrame = False
				if not inFrame and next[0] == 0xBE:
					if self.serialComm.read(1)[0] == 0xEE:
						inFrame = True
						recvBuffer = b"\xBE\xEE"
		except:
			self.rxThreadEnabled = False

	def initSerialComm(self):
		self.serialComm = None
		try:
			self.serialComm = Serial(self.port,115200)
			time.sleep(1)
		except SerialException:
			print("Error: device not found !")
			exit(1)

	def enableRxThread(self):
		self.rxThreadEnabled = True
		self.rxThread = Thread(target=self._rxThread, args=[])
		self.rxThread.daemon=True
		self.rxThread.start()


	def receivePackets(self,pcapFile=None):
		if pcapFile is not None:
			pcapWriter = PCAPWriter(pcapFile)
			pcapMode = pcapWriter.open()
		else:
			pcapMode = False

		if pcapMode:
			pcapWriter.addHeader()
		while True:
			if not self.frameQueue.empty():
				frame = self.frameQueue.get()
				timestamp = time.time()
				print(str(timestamp)+": "+' '.join(['{:02x}'.format(i) for i in frame.data])+" (FCS: "+("NOK" if frame.fcs_ok == 0 else "OK")+")")
				if pcapMode:
					pcapWriter.addPacket(bytes(frame.data)[2:],timestamp)

		
	def sendCommand(self, command):
		self.serialComm.write(raw(Wazabee_Hdr()/Wazabee_Command_Hdr()/command))

	def getFirmwareVersion(self):
		self.sendCommand(Wazabee_Command_Get_Firmware_Version())
		response = None
		while response is None or response.response_type != 0:
			response = self.commandQueue.get()
		return (response.major, response.minor, "TI CC1352-R1" if response.device == 0x0B else "NRF52832")

	def getFCSMode(self):
		self.sendCommand(Wazabee_Command_Get_FCS_Mode())
		response = None
		while response is None or response.response_type != 1:
			response = self.commandQueue.get()
		return "all" if response.mode == 0x00 else "valid_fcs_only"


	def setFCSMode(self,mode="all"):
		self.sendCommand(Wazabee_Command_Set_FCS_Mode(mode=0x00 if mode == "all" else 0x01))
		response = None
		while response is None or response.response_type != 2:
			response = self.commandQueue.get()
		return response.success == 0x00


	def getChannel(self):
		self.sendCommand(Wazabee_Command_Get_Channel())
		response = None
		while response is None or response.response_type != 3:
			response = self.commandQueue.get()
		return response.channel

	def setChannel(self,channel):
		self.sendCommand(Wazabee_Command_Set_Channel(channel=channel))
		response = None
		while response is None or response.response_type != 4:
			response = self.commandQueue.get()
		return response.success == 0x00

	def sendPacket(self, packet, calcFcs = False):

		print("Transmitting: "+' '.join(['{:02x}'.format(i) for i in packet])+" (FCS:"+("auto" if calcFcs else "{:02x} {:02x}".format(packet[-1],packet[-2]))+")")
		self.sendCommand(Wazabee_Command_Send_Packet(data=bytes(packet),calc_fcs=(0x01 if calcFcs else 0x00)))
		response = None
		while response is None or response.response_type != 5:
			response = self.commandQueue.get()
		return True

	def reset(self):
		self.sendCommand(Wazabee_Command_Reset())
		response = None
		while response is None or response.response_type != 6:
			response = self.commandQueue.get()
		return True

	def stop(self):
		self.rxThreadEnabled = False
		self.serialComm.close()
		exit(0)
