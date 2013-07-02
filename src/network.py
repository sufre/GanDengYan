import socket
import asyncore

class Client(asyncore.dispatcher):
	"""network client"""
	callback = None
	buffer = ''

	def __init__(self, callback, sock=None, host='', port=''):
		self.callback = callback
		if sock is None:
			asyncore.dispatcher.__init__(self)
			self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connect((host, port))
		else:
			asyncore.dispatcher.__init__(self, sock)

	def write(self, content):
		self.buffer = self.buffer + content

	def writable(self):
		return (len(self.buffer) > 0)

	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]

	def handle_read(self):
		recv = self.recv(8192)
		if self.callback is not None:
			self.write(self.callback(recv))
		else:
			self.write('{\'errmsg\':\'client no callback\'}')


class Server(asyncore.dispatcher):
	"""network server"""
	callback = None
	def __init__(self, callback, host, port):
		self.callback = callback
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			print 'Incoming connection from %s' % repr(addr)
			client = Client(self.callback, sock)
		
