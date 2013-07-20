import json
import time

import clientUi
import gameLogic
import gameUtils

class Msg:
	"""interface for Msg"""
	fromEnd = ''
	toEnd = ''

	msgId = 0
	msgFrom = ''
	msgTo = ''
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

	def process(self, params):
		pass

	def result(self, params):
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
		

		
class LoginMsg(Msg):
	"""login"""
	username = ''

	def __init__(self, msg=None):
		self.fromEnd = 'client'
		self.toEnd = 'server'

		self.initErrCodes()

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

		self.msgFrom = ''
		self.msgTo = 'server'
		
		self.msgParams['name'] = params['name']
		return self

	def process(self, params):
		#game for serverEnd logic
		server = params
		if server.addPlayer(self.msgParams['name']):
			self.setErrCode(0)
		else:
			self.setErrCode(1)
		return self

	def result(self, params):
		#ui for clientEnd user interface
		ui = params
		if self.msgResults['errCode'] == 0:
			ui.rawoutput('login success!')
		else:
			ui.rawoutput('login fail, server may not exsit, please contact z00214951.')
		return None

class GameStatusMsg(Msg):
	def __init__(self, msg=None):
		self.fromEnd = 'server'
		self.toEnd = 'client'

		self.initErrCodes()

		if msg is not None:
			self.msgId = msg.msgId
			self.msgFrom = msg.msgFrom
			self.msgTo = msg.msgTo
			self.msgMethod = msg.msgMethod
			self.msgParams = msg.msgParams
			self.msgResults = msg.msgResults

	def initErrCodes(self):
		self.errCodes.append((1, 'Unkown message'))

	def make(self, params):
		#for fromEnd
		self.msgId = int(time.time())
		self.msgMethod = 'gameStatus'

		self.msgFrom = 'server'
		self.msgTo = params['to']
		
		self.msgParams['status'] = params['status']
		if 'lefts' in params:
			self.msgParams['lefts'] = params['lefts']
		self.msgParams['players'] = params['players']
		return self

	def process(self, params):
		#game for serverEnd logic
		ui = params
		ui.clear()

		for player in self.msgParams['players']:
			ui.addPlayer(player)

		if self.msgParams['status'] == 'gaming':
			if 'lefts' in self.msgParams:
				ui.gamingLog(self.msgParams['lefts'])
			for player in self.msgParams['players']:
				if 'isTurn' in self.msgParams['players'][player]:
					if self.msgParams['players'][player]['isTurn'] == 'true':
						ui.changeTurn(player)
				if player == self.msgTo:
					ui.setCards(self.msgParams['players'][player]['cards'])
				ui.changePlayerContent(player, gameUtils.joinCards(self.msgParams['players'][player]['posts']))
		else:
			for player in self.msgParams['players']:
				if 'isReady' in self.msgParams['players'][player]:
					if self.msgParams['players'][player]['isReady'] == 'true':
						ui.getPlayer(player).ready()
		ui.output()
		self.setErrCode(0)
		return self

	def result(self, params):
		#ui for clientEnd user interface
		pass

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
		return LoginMsg(msg)

def test(msgType):
	if msgType == 'login':
		params = {}
		params['clientid'] = 1
		params['name'] = 'sufre'
		Loginmsg = LoginMsg().make(params)
		print 'make test: ' + Loginmsg.toString()
		msg = loads(Loginmsg.toString())
		print 'msg loads: ' + msg.toString()

test('login')