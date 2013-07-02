import network

def process(message):
	print message
	return ''

client = network.Client(process, None, 'localhost', 33333)
client.write('hello world')
network.asyncore.loop()