import socket
import binascii
import struct
import sys
import logging

def ten_digit_to_comma_format(badge):
	"""Returns the comma-format RFID number (without the comma) from the 10-digit RFID number
	
	Explanation:
	*On an EM4100/4001 spec RFID card generally there will be a two sets of numbers like this: 0015362878 234,27454
	*The part of the number before the comma represents the first hex byte of the "10 digit" number, and the second part is the last 2 hex bytes of the "10 digit" card number. 
	*15362878 = EA6B3E
	*Splitting EA and 6B3E and converting them to a decimal numbers will give you 234 and 27454 (the number with the comma on the card).
	*The comma is excluded in the return value because the controller does not need the comma.
	
	:param badge: 10-digit RFID card number, must be integer
	"""
	if badge > 16777215: # only the last 8 digits are the ID, and the 8 digits correspond to only 6 hex values, so the max is FFFFFF
		Exception("Error: Invalid RFID Number")
	formattedID = str("{0:x}".format(badge)).zfill(6) # converts to hex
	return int(str(int(formattedID[:2], 16)).zfill(3) + str(int(formattedID[-4:], 16)).zfill(5)) # splits the hex at first two and last 4, converts to dec, then combines into string


def comma_format_to_ten_digit(badge):
	"""Returns the 10-digit number from the comma-format RFID number (without the comma)
	
	Explanation:
	*On an EM4100/4001 spec RFID card generally there will be a two sets of numbers like this: 0015362878 234,27454
	*This function turns the number with the comma (but excluding the comma) into the 10-digit number which is generally next to it.
	*The part of the number before the comma represents the first hex byte of the "10 digit" number, and the second part is the last 2 hex bytes of the "10 digit" card number. 
	**234 = EA
	**27454 = 6B3E
	**Combining EA and 6B3E and converting it to a decimal number will give you 15362878 (the first 10-digit number on the card).
	
	:param badge: comma-format RFID card number, must be integer with the comma removed
	"""
	if badge > 25565535: # the 8 digits correspond to a set of two and four hex values, so the max is the decimal version of FF and FFFF concatenated
		Exception("Error: Invalid RFID Number")
	badge = str(badge).zfill(8)
	formattedID = "{0:x}".format(int(badge[:-5])).zfill(2) + "{0:x}".format(int(badge[-5:])).zfill(4) # splits dec at last 5 digits and everything except last 5, converts each section to hex, then combines
	return int(formattedID, 16) # converts combined hex string to int


class RFIDClient():
	def __init__(self, ip, serial):
		"""
		:param ip: IP address of the controller.
		:param serial: Serial number written on the controller, also "Device NO" on the web interface's configuration page.
		"""
		try:
			socket.inet_aton(ip)
		except socket.error:
			raise TypeError("IP Address is not valid")
		if not isinstance(serial, int):
			raise TypeError("Serial must be set to an integer")
			
		self.controller_serial = struct.pack('<I', serial).encode('hex') # pack as little endian integer
		self.s = self.connect(ip)
		self.source_port = '0000' # the part of the byte string replaced by the CRC, not required to be valid
		self.start_transaction = '0d0d0000000000000000000000000000000000000000000000000000'.decode('hex') # this byte starts a transaction


	def connect(self, ip, timeout=5, port=60000):
		"""
		:param ip: IP address of the controller
		:param timeout: settimeout value for the sockets connection
		:param port: the destination port of the socket, should always be 60000
		"""
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
			s.connect((ip, port))
			s.settimeout(timeout)
		except Exception as e:
			print(e)
			sys.exit(1)
		return s


	def CRC_16_IBM(self, data):
		""" Returns hex string with CRC values added to positions 4 through 8. This CRC value is required by the controller or it will not process the request.
		
		:param data: original hex string which needs the CRC values added to it
		"""
		hex_data = data.decode("hex")
		byteList = map(ord, hex_data)
		num1 = 0
		for i in xrange(0, len(byteList)):
			num2 = byteList[i]
			if i == 2 or i == 3:
				num2 = 0
			num1 ^= num2
			for j in xrange(0, 8):
				if num1&1 > 0:
					num1 = (num1>>1)^40961
				else:
					num1 >>= 1
		code = num1 &65535 # integer returned from CRC function
		
		listString = list(data) # change hex string to list to support assignment
		listString[4:8] = struct.pack('<H', code).encode('hex') # switch order to little endian and return unsigned short, then replace characters in list with the CRC values
		return "".join(listString) 


	def add_user(self, badge, doors):
		if not isinstance(badge, int):
			raise TypeError("RFID number must be set to an integer")
			
		if not isinstance(doors, list):
			raise Exception("doors must be set to a list")
		
		# create a list of "01"'s (enabled) and "00"'s (disabled), then later join to create "01000000" (which is only door 1 enabled)
		doorsList = []
		doorsList.append("01") if 1 in doors else doorsList.append("00") # door 1
		doorsList.append("01") if 2 in doors else doorsList.append("00") # door 2
		doorsList.append("01") if 3 in doors else doorsList.append("00") # door 3
		doorsList.append("01") if 4 in doors else doorsList.append("00") # door 4
			
		badge = struct.pack('<I', badge).encode('hex') # pack as little endian integer
		
		add_packet1 = self.CRC_16_IBM('2010' + self.source_port + '2800000000000000' + self.controller_serial + '00000200ffffffff').decode('hex')
		self.s.send(self.start_transaction)
		self.s.send(add_packet1)
		recv_data1 =  binascii.b2a_hex(self.s.recv(1024))
		if (recv_data1[:4] != '2011'):
			raise Exception("Unexpected Result Received: %s" % recv_data1)
			
		add_packet2 = self.CRC_16_IBM('2320' + self.source_port + '2900000000000000' + self.controller_serial + '00000200' + badge + '00000000a04e4605' + '87' + '1c9f3b' + "".join(doorsList) + '00000000').decode('hex')
		self.s.send(self.start_transaction)
		self.s.send(add_packet2)
		recv_data2 =  binascii.b2a_hex(self.s.recv(1024))
		if (recv_data2[:4] != '2321'):
			raise Exception("Unexpected Result Received: %s" % recv_data2)


	def remove_user(self, badge):
		if not isinstance(badge, int):
			raise TypeError("RFID number must be set to an integer")
			
		badge = struct.pack('<I', badge).encode('hex') # pack as little endian integer
		
		remove_packet = self.CRC_16_IBM('2320' + self.source_port + '2200000000000000' + self.controller_serial + '00000200' + badge + '00000000204e460521149f3b0000000000000000').decode('hex')
		self.s.send(self.start_transaction)
		self.s.send(remove_packet)
		recv_data =  binascii.b2a_hex(self.s.recv(1024))
		if (recv_data[:4] != '2321'):
			raise Exception("Unexpected Result Received: %s" % recv_data)
			
	def open_door(self, door_number):
		if not isinstance(door_number, int):
			raise TypeError("RFID number must be set to an integer")
		if not (1 <= door_number <= 4):
			raise Exception("door_number must be 1 to 4")
				
		door_number = str(door_number - 1).zfill(2)
		
		open_door_packet = self.CRC_16_IBM("2040" + self.source_port + "0500000000000000" + self.controller_serial + "0000020001000000ffffffffffffffff" + door_number + "000000").decode('hex')
		self.s.send(self.start_transaction)
		self.s.send(open_door_packet)
		recv_data =  binascii.b2a_hex(self.s.recv(1024))
		if (recv_data[:4] != '2041'):
			raise Exception("Unexpected Result Received: %s" % recv_data)


	def remove_all(self):
		rma_packet1 = self.CRC_16_IBM('2120' + self.source_port + '7600000000000000' + self.controller_serial + '0000020000100000ff130000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff').decode('hex')
		self.s.send(self.start_transaction)	
		self.s.send(rma_packet1)
		recv_data1 =  binascii.b2a_hex(self.s.recv(1024))
		if (recv_data1[:4] != '2121'):
			raise Exception("Unexpected Result Received: %s" % recv_data1)
                setentrynumber = '00'
		rma_packet2 = self.CRC_16_IBM('2330' + self.source_port + '7900000000000000' + self.controller_serial + '0000020000000000000000009812000001000000' + setentrynumber + '0000000000000000800c0000900c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000').decode('hex')
		self.s.send(self.start_transaction)
		self.s.send(rma_packet2)
		recv_data2 =  binascii.b2a_hex(self.s.recv(1024))
		if (recv_data2[:4] != '2331'):
			raise Exception("Unexpected Result Received: %s" % recv_data2)


	def set_passwords(self, pass_1, pass_2, pass_3, pass_4): #for example if password is 123569 Hex is 01e2b1 and pxa='01' pxb='e2' pxc='b1'
			
		if not (0 <= len(pass_1) <= 6) or not (0 <= len(pass_2) <= 6) or not (0 <= len(pass_3) <= 6) or not (0 <= len(pass_4) <= 6):
			raise Exception("passwords must be between 1 and 6 characters")

		hexpass_1 = struct.pack('<i', int(pass_1)).encode('hex')
		hexpass_2 = struct.pack('<i', int(pass_2)).encode('hex')
		hexpass_3 = struct.pack('<i', int(pass_3)).encode('hex')
		hexpass_4 = struct.pack('<i', int(pass_4)).encode('hex')		

		if not (int(pass_1) > 0):

			p1a = 'ff' 		
			p1b = 'ff' 		
			p1c = 'ff' 		
		else:
			p1a = str(hexpass_1[4:6]) 		#two first hex from pass_1 XXxxxx
			p1b = str(hexpass_1[2:4]) 		#two second hex from pass_1 xxXXxx
			p1c = str(hexpass_1[0:2]) 		#two third hex from pass_1 xxxxXX

		if not (int(pass_2) > 0):

			p2a = 'ff'
			p2b = 'ff'
			p2c = 'ff'
		else:
			p2a = str(hexpass_2[4:6])
			p2b = str(hexpass_2[2:4])
			p2c = str(hexpass_2[0:2])

		if not (int(pass_3) > 0):

			p3a = 'ff'
			p3b = 'ff'
			p3c = 'ff'
		else:
			p3a = str(hexpass_3[4:6])
			p3b = str(hexpass_3[2:4])
			p3c = str(hexpass_3[0:2])

		if not (int(pass_4) > 0):

			p4a = 'ff'
			p4b = 'ff'
			p4c = 'ff'
		else:

			p4a = str(hexpass_4[4:6])
			p4b = str(hexpass_4[2:4])
			p4c = str(hexpass_4[0:2])

		set_passwords = self.CRC_16_IBM("2420" + self.source_port + "0400000000000000" + self.controller_serial + "000002000d7e1e001e001e001e0003030303000000000102030400000000ff00ff000000000008fa006400ff55011e00007e1e1e0000ffff0000ffff0000000000043200ffffffffffffffffffff8494"+p1c+p1b+p2c+p2b+p3c+p3b+p4c+p4b+"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc0a80000ffff0000c0a8000060ea0000000000000000000000000000000000000000000000000000000000000000000d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffffffff49ee4aee000000000000ff"+p1a+p2a+p3a+p4a+"ffffffffffffffffffffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000cc4c3e049f9339f00fcffffff0f000000fffffffff10f00007000c4ffff0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000").decode('hex')
		self.s.send(self.start_transaction)
		self.s.send(set_passwords)
		recv_data =  binascii.b2a_hex(self.s.recv(1024))
		if (recv_data[:4] != '2421'):
			raise Exception("Unexpected Result Received: %s" % recv_data)

	
	def __del__(self):
		"""
		Closes the socket connection.
		"""
		self.s.close()
