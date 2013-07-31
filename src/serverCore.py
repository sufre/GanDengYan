import cmd
import threading
import gameLogic
import network
import message



class ServerCore(cmd.Cmd):
	server = None

	game = None

	unhandledClients = []

	clients = {}

	currentClient = None

	def __init__(self, host, port):
		cmd.Cmd.__init__(self)
		self.server = network.Server(self.process, self.accept, host, port)
		self.game = gameLogic.Game()

	def start(self):
		threading.Thread(target=network.asyncore.loop, kwargs={'timeout':0.1}).start()
		cmd.Cmd.cmdloop(self)

	def do_exit(self, line):
		print 'going to exit...'
		network.asyncore.close_all()
		return True

	def accept(self, client):
		self.unhandledClients.append(client)

	def process(self, msg, client):
		result = ''
		self.currentClient = client
		recvMsg = message.loads(msg)
		while recvMsg is not None:
			if recvMsg.toEnd == 'server':
				result = result + recvMsg.process(self).toResultString()
			else:
				recvMsg.result(self)
			recvMsg = message.loads('')
		

	def addPlayer(self, name):
		client = self.currentClient
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
			self.unhandledClients.pop(pos)

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
				params['to'] = cl
				self.clients[cl].write(message.GameStatusMsg().make(params).toParamString())

			return True
		return False

server = ServerCore('localhost', 33333)
server.start()