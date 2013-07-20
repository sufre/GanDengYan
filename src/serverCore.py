import gameLogic
import network
import message



class ServerCore:
	server = None

	game = None

	unhandledClients = []

	clients = {}

	self.currentClient = None

	def __init__(self, host, port):
		self.server = network.Server(self.process, self.accept, host, port)
		self.game = gameLogic.Game()

	def accept(self, client):
		unhandledClients.append(client)

	def process(self, msg, client):
		recvMsg = message.loads(msg)
		if recvMsg.toEnd == 'server':
			return recvMsg.process(self).toResultString()
		else:
			recvMsg.result(self)
			return ''

	def addPlayer(self, name, client):
		if self.game.addPlayer(name):
			pos = 0
			for unhandledClient in self.unhandledClients:
				if unhandledClient is client:
					break
				pos = pos + 1
			if pos == len(self.unhandledClients):
				self.game.delPlayer(name)
				return False
			self.clients[name] = client

			#notify others someone login
			params = {}
			if self.game.isStart:
				params['status'] = 'gaming'
				params['lefts'] = len(self.game.leftCards)
			else:
				params['status'] = 'wait'

			params['players'] = {}
			for player in self.game.players:
				params['players'][player.name] = {}
				if player.isReady:
					params['players'][player.name]['isReady'] = 'true'
				if player.isTurn:
					params['players'][player.name]['isTurn'] = 'true'
				params['players'][player.name]['cards'] = player.owns
				params['players'][player.name]['posts'] = player.post
			for cl in self.clients:
				self.clients[cl].write(message.GameStatusMsg().make(params).toParamString())

			return True
		return False
