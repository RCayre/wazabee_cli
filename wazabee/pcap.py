import time
from struct import pack,unpack

DLT = 195

class PCAPWriter:
	def __init__(self,filename):
		self.filename = filename
		self.fileDescriptor = None

	def open(self):
		try:
			self.fileDescriptor = open(self.filename,"wb")
			return True
		except:
			self.fileDescriptor = None
			return False

	def addHeader(self):
		magic = 0xa1b2c3d4
		header = pack('<IHHIIII',
			magic,
			2,
			4,
			0,
			0,
			65535,
			DLT
		)
		try:
			self.fileDescriptor.write(header)
			return True
		except:
			return False



	def addPacket(self,data,timestamp=None):
		try:
			if timestamp is None:
				timestamp = time.time()
			ts_sec = int(timestamp)
			ts_usec = int((timestamp - ts_sec)*1000000)
			header = pack(
			'<IIII',
			ts_sec,
			ts_usec,
			len(data),
			len(data)
			)
			self.fileDescriptor.write(header)
			self.fileDescriptor.write(data)
			return True
		except:
			return False

	def close(self):
		self.fileDescriptor.close()

	def __del__(self):
		if self.fileDescriptor is not None:
			self.close()


class PCAPReader:
	def __init__(self,filename):
		self.filename = filename
		self.fileDescriptor = None

	def open(self):
		try:
			self.fileDescriptor = open(self.filename,"rb")
			return True
		except:
			self.fileDescriptor = None
			return False

	def checkHeader(self):
		try:
			header = self.fileDescriptor.read(24)
			magic,*others,dlt =  unpack('<IHHIIII',header)
			return 0xa1b2c3d4 == magic and DLT == dlt
		except:
			return False

	def getFrame(self):
		try:
			header = self.fileDescriptor.read(16)
			ts_sec, ts_usec, length1, length2 = unpack('<IIII',header)
			packet = self.fileDescriptor.read(length1)
			return (True,(ts_sec + ts_usec/1000000,packet))

		except:
			return (False,None)

	def getFrames(self):
		frames = []
		content = True
		while content:
			content,data = self.getFrame()
			if content:
				frames += [data]
		return frames


	def close(self):
		self.fileDescriptor.close()

	def __del__(self):
		if self.fileDescriptor is not None:
			self.close()

