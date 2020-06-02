from scapy.all import Packet, bind_layers
from scapy.fields import *

class Wazabee_Hdr(Packet):
	name = "WazaBee Packet"
	fields_desc = [
		XShortField("preamble", 0xBEEE),
		ByteEnumField("type", None, {0:"command", 1:"response", 2:"packet"})
	]

class Wazabee_Command_Hdr(Packet):
	name = "WazaBee Command Packet"
	fields_desc = [
		ByteEnumField("command_type", None, {0:"getFirmwareVersion", 1:"getFCSMode", 2:"setFCSMode", 3:"setChannel", 4:"getChannel" , 5:"sendPacket", 6 : "reset" })
	]

class Wazabee_Command_Get_Firmware_Version(Packet):
	name = "Wazabee Command Get Firmware Version"
	fields_desc = []

class Wazabee_Command_Get_FCS_Mode(Packet):
	name = "Wazabee Get FCS Mode"
	fields_desc = []

class Wazabee_Command_Set_FCS_Mode(Packet):
	name = "Wazabee Set FCS Mode"
	fields_desc = [ByteEnumField("mode",None, {0x00 : "all", 0x01 : "valid_fcs_only"})]

class Wazabee_Command_Set_Channel(Packet):
	name = "Wazabee Command Set Channel"
	fields_desc = [ByteField("channel",11)]

class Wazabee_Command_Get_Channel(Packet):
	name = "Wazabee Command Get Channel"
	fields_desc = []

class Wazabee_Command_Send_Packet(Packet):
	name = "Wazabee Command Send Packet"
	fields_desc = [
		ByteEnumField("calc_fcs", None, {0x00 : "no", 0x01 : "yes"}),
		FieldLenField("data_size", None, length_of="data", fmt="B"),
		StrLenField("data", "", length_from = lambda pkt: pkt.data_size)
	]

class Wazabee_Command_Reset(Packet):
	name = "Wazabee Command Reset"
	fields_desc = []

class Wazabee_Response_Hdr(Packet):
	name = "WazaBee Response Packet"
	fields_desc = [
		ByteEnumField("response_type", None, {0:"getFirmwareVersion", 1:"getFCSMode", 2:"setFCSMode", 3:"setChannel", 4:"getChannel" , 5:"sendPacket", 6 : "reset" })
	]

class Wazabee_Response_Get_Firmware_Version(Packet):
	name = "WazaBee Get Firmware Version"
	fields_desc = [
		ByteField("major",None), 
		ByteField("minor",None),
		ByteEnumField("device",None, {0x0A: "NRF52832",0x0B:"TI CC1352-R1"})
	]

class Wazabee_Response_Get_FCS_Mode(Packet):
	name = "Wazabee Get FCS Mode"
	fields_desc = [ByteEnumField("mode",None, {0x00 : "all", 0x01 : "valid_fcs_only"})]

class Wazabee_Response_Set_FCS_Mode(Packet):
	name = "Wazabee Set FCS Mode"
	fields_desc = [ByteEnumField("success",None, {0: "success", 1: "failure"})]


class Wazabee_Response_Set_Channel(Packet):
	name = "WazaBee Response Set Channel"
	fields_desc = [
		ByteEnumField("success",None, {0: "success", 1: "failure"})
	]

class Wazabee_Response_Get_Channel(Packet):
	name = "WazaBee Response Get Channel"
	fields_desc = [
		ByteField("channel",None)
	]


class Wazabee_Response_Send_Packet(Packet):
	name = "Wazabee Response Send Packet"
	fields_desc = [
	]

class Wazabee_Response_Reset(Packet):
	name = "Wazabee Response Reset"
	fields_desc = []


class Wazabee_Packet(Packet):
	name = "Wazabee Packet"
	fields_desc = [
		FieldLenField("data_size", None, length_of="data",fmt="B"),
		StrLenField("data", "", length_from = lambda pkt: pkt.data_size),
		ByteEnumField("fcs_ok", None, {0: "no", 1:"yes"})
	]



bind_layers(Wazabee_Hdr,Wazabee_Command_Hdr, 	type = 0)
bind_layers(Wazabee_Hdr,Wazabee_Response_Hdr, 	type = 1)
bind_layers(Wazabee_Hdr,Wazabee_Packet, 	type = 2)

bind_layers(Wazabee_Command_Hdr,Wazabee_Command_Get_Firmware_Version, 	command_type = 0)
bind_layers(Wazabee_Command_Hdr,Wazabee_Command_Get_FCS_Mode, 		command_type = 1)
bind_layers(Wazabee_Command_Hdr,Wazabee_Command_Set_FCS_Mode, 		command_type = 2)
bind_layers(Wazabee_Command_Hdr,Wazabee_Command_Get_Channel, 		command_type = 3)
bind_layers(Wazabee_Command_Hdr,Wazabee_Command_Set_Channel, 		command_type = 4)
bind_layers(Wazabee_Command_Hdr,Wazabee_Command_Send_Packet, 		command_type = 5)
bind_layers(Wazabee_Command_Hdr,Wazabee_Command_Reset,	 		command_type = 6)

bind_layers(Wazabee_Response_Hdr,Wazabee_Response_Get_Firmware_Version, response_type = 0)
bind_layers(Wazabee_Response_Hdr,Wazabee_Response_Get_FCS_Mode, 	response_type = 1)
bind_layers(Wazabee_Response_Hdr,Wazabee_Response_Set_FCS_Mode, 	response_type = 2)
bind_layers(Wazabee_Response_Hdr,Wazabee_Response_Get_Channel, 		response_type = 3)
bind_layers(Wazabee_Response_Hdr,Wazabee_Response_Set_Channel,		response_type = 4)
bind_layers(Wazabee_Response_Hdr,Wazabee_Response_Send_Packet, 		response_type = 5)
bind_layers(Wazabee_Response_Hdr,Wazabee_Response_Reset, 		response_type = 6)
