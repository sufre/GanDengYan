import network
import message

class ClientCore:
	"""client logic core"""
	sockClient = None

	def __init__(self, host, port):
		sockClient = network.Client(self.process, None, host, port)

	def process(self, msg):
		response = ''
		return response
