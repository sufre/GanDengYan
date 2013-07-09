import json
import time

class Msg:
	"""interface for Msg"""
	fromEnd = ''
	toEnd = ''

	msgId = ''
	msgFrom = ''
	msgTo = ''
	msgMethod = ''
	msgParams = ''
	msgResults = ''

	def __init__(self, clientId):
		

	def make(self, params):
		jsonMsg = {}
		msgId = time.time()
		jsonMsg['id'] = msgId


		
class loginMsg(Msg):
	"""login"""
	username = ''

	def __init__(self):
		self.fromEnd = 'client'
		self.toEnd = 'server'
	
	def make	


class MsgManager:
	"""msg process module"""
	def __init__(self, mode):
		self.mode = mode
		if self.mode is 'client':


		