import cmd
import network
import message

import clientUi


class ClientCore(cmd.Cmd):
	"""client logic core"""
	sockClient = None

	ui = None

	def __init__(self, host, port):
		self.sockClient = network.Client(self.process, None, host, port)
		self.ui = clientUi.Ui()

	def process(self, msg, client):
		recvMsg = message.loads(msg)
		if recvMsg.toEnd == 'client':
			return recvMsg.process(self.ui).toResultString()
		else:
			responseMsg = recvMsg.result(self.ui)
			if responseMsg is not None:
				return responseMsg.toParamString()
			return ''

	def do_login(self, line):
		params = {}
		params['name'] = line
		self.sockClient.write(message.LoginMsg().make(params).toString())
