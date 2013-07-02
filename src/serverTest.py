import network

def process(message):
	print message
	return ''

server = network.Server(process, 'localhost', 33333)
network.asyncore.loop()