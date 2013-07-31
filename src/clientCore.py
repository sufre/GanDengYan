import cmd
import threading

import network
import message

import clientUi


class ClientCore(cmd.Cmd):
	"""client logic core"""
	sockClient = None

	ui = None

	def __init__(self, host, port):
		cmd.Cmd.__init__(self)
		self.sockClient = network.Client(self.process, None, host, port)
		self.ui = clientUi.Ui()

	def start(self):
		threading.Thread(target=network.asyncore.loop, kwargs={'timeout':0.1}).start()
		cmd.Cmd.cmdloop(self)

	def process(self, msg, client):
		result = ''
		recvMsg = message.loads(msg)
		while recvMsg is not None:
			if recvMsg.toEnd == 'client':
				result = result + recvMsg.process(self.ui).toResultString()
			else:
				responseMsg = recvMsg.result(self.ui)
				if responseMsg is not None:
					result = result + responseMsg.toParamString()
			recvMsg = message.loads('')

	def do_login(self, line):
		params = {}
		params['name'] = line
		self.sockClient.write(message.LoginMsg().make(params).toString())

	def do_exit(self, line):
		print 'going to exit...'
		network.asyncore.close_all()
		return True

client = ClientCore('localhost', 33333)
client.start()
