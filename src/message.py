import json
import time

class Msg:
	"""interface for Msg"""
	fromEnd = ''
	toEnd = ''

	msgId = 0
	msgFrom = 0
	msgTo = 0
	msgMethod = {}
	msgParams = {}
	msgResults = {}

	def __init__(self):
		pass

	def make(self, params):
		pass

	def process(self, msg, params):
		pass

	def result(self, msg, params):
		pass

	def toString(self):
		jsonMsg = {}
		jsonMsg['id'] = self.msgId
		jsonMsg['from'] = self.msgFrom
		jsonMsg['to'] = self.msgTo
		jsonMsg['method'] = self.msgMethod
		if len(self.msgParams) is not 0:
			jsonMsg['params'] = self.msgParams
		if len(self.msgResults) is not 0:
			jsonMsg['results'] = self.msgResults
		return json.dumps(jsonMsg)
		

		
class loginMsg(Msg):
	"""login"""
	username = ''

	def __init__(self, msg=None):
		self.fromEnd = 'client'
		self.toEnd = 'server'

		if msg is not None:
			self.msgId = msg.msgId
			self.msgFrom = msg.msgFrom
			self.msgTo = msg.msgTo
			self.msgMethod = msg.msgMethod
			self.msgParams = msg.msgParams
			self.msgResults = msg.msgResults
	
	def make(self, params):
		self.msgId = int(time.time())
		self.msgMethod = 'login'

		self.msgFrom = params['clientid']
		self.msgTo = 0
		
		self.msgParams['name'] = params['name']
		return self

def loads(strMsg):
	msg = Msg()
	jsonMsg = json.loads(strMsg)
	msg.msgId = jsonMsg['id']
	msg.msgFrom = jsonMsg['from']
	msg.msgTo = jsonMsg['to']
	msg.msgMethod = jsonMsg['method']
	if 'params' in jsonMsg:
		msg.msgParams = jsonMsg['params']
	if 'results' in jsonMsg:
		msg.msgResults = jsonMsg['results']

	if msg.msgMethod == 'login':
		return loginMsg(msg)

params = {}
params['clientid'] = 1
params['name'] = 'sufre'
loginmsg = loginMsg().make(params)
msg = loads(loginmsg.toString())
print msg.toString()