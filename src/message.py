import json
import time

import clientUi
import gameLogic

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

	errCodes = [(0, '')]

	def __init__(self):
		pass

	#errcodes
	def initErrCodes(self):
		pass

	def setErrCode(self, errCode):
		for err in self.errCodes:
			code, desc = err
			if code == errCode:
				self.msgResults['errCode'] = code
				self.msgResults['errDesc'] = desc
				return True
		return False

	#callbacks
	def make(self, params):
		pass

	def process(self, game):
		pass

	def result(self, ui):
		pass

	#toStrings
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

	def toParamString(self):
		jsonMsg = {}
		jsonMsg['id'] = self.msgId
		jsonMsg['from'] = self.msgFrom
		jsonMsg['to'] = self.msgTo
		jsonMsg['method'] = self.msgMethod
		jsonMsg['params'] = self.msgParams
		return json.dumps(jsonMsg)

	def toResultString(self):
		jsonMsg = {}
		jsonMsg['id'] = self.msgId
		jsonMsg['from'] = self.msgFrom
		jsonMsg['to'] = self.msgTo
		jsonMsg['method'] = self.msgMethod
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

	def initErrCodes(self):
		self.errCodes.append((1, 'Name conflict'))
	
	def make(self, params):
		#for fromEnd
		#params should has: 'clientid' for const -1, 'name' for loginName
		self.msgId = int(time.time())
		self.msgMethod = 'login'

		self.msgFrom = params['clientid']
		self.msgTo = 0
		
		self.msgParams['name'] = params['name']
		return self

	def process(self, game):
		#game for serverEnd logic
		if game.addPlayer(self.msgParams['name']):
			self.setErrCode(0)
			self.msgResults['id'] = game.getId()
		else:
			self.setErrCode(1)
		return self

	def result(self, ui):
		#ui for clientEnd user interface
		if self.msgResults['errCode'] == 0:
			ui.rawoutput('login success!')
		else:
			ui.rawoutput('login fail, server may not exsit, please contact z00214951.')

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

def test(msgType):
	if msgType == 'login':
		params = {}
		params['clientid'] = 1
		params['name'] = 'sufre'
		loginmsg = loginMsg().make(params)
		print 'make test: ' + loginmsg.toString()
		msg = loads(loginmsg.toString())
		print 'msg loads: ' + msg.toString()

test('login')