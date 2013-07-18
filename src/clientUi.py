
class Player:

	name = ''

	playerStatus = ''

	playerContent = ''

	def __init__(self, name):
		self.name = name
		self.unready()
		self.setContent('')

	def ready(self):
		self.playerStatus = '  READY '

	def unready(self):
		self.playerStatus = 'UNREADY '

	def onTurn(self):
		self.playerStatus = '      * '

	def offTurn(self):
		self.playerStatus = '        '

	def setContent(self, content):
		self.playerContent = '(' + content + '\t' + ')'



class Ui:

	gameStatus = ''

	gameLog = ''

	playerList = []

	def __init__(self):
		self.wait()
		self.waitLog()

	def addPlayer(self, name):
		self.playerList.append(Player(name))

	def delPlayer(self, name):
		pos = 0
		for player in self.playerList:
			if player.name == name:
				break
			pos = pos + 1
		if pos != len(self.playerList):
			self.playerList.pop(pos)

	def getPlayer(self, name):
		for player in self.playerList:
			if player.name == name:
				return player
		return None

	def wait(self):
		self.gameStatus = 'Wait'
		self.waitLog()
		for player in self.playerList:
			player.unready()
			player.setContent('')

	def gaming(self):
		self.gameStatus = 'Gaming'
		self.startLog()
		for player in self.playerList:
			player.offTurn()
			player.setContent('')

	def waitLog(self):
		self.gameLog = 'Game is not start'

	def startLog(self):
		self.gameLog = 'Prepare for game'

	def gamingLog(self, leftCardNum):
		self.gameLog = str(leftCardNum) + ' cards left'

	def changeTurn(self, name):
		for player in self.playerList:
			player.offTurn()
			if player.name == name:
				player.onTurn()

	def changePlayerContent(self, name, content):
		for player in self.playerList:
			if player.name == name:
				player.setContent(content)

	def output(self):
		print ''
		print '---------------------------------150 Gaming---------------------------------'
		print self.gameStatus + '\t\t|\t' + self.gameLog
		print '----------------------------------------------------------------------------'
		formatStr = ''
		for player in self.playerList:
			formatStr = formatStr + player.playerStatus + player.name + player.playerContent + '\t'
		print formatStr
		print '----------------------------------------------------------------------------'

	def rawoutput(self, content):
		print content

def test():
	print '################# player ui test #################'
	ui = Ui()

	#addplayer
	ui.addPlayer('A')
	ui.addPlayer('B')
	ui.addPlayer('C')
	ui.output()

	#someone is ready
	a = ui.getPlayer('A')
	a.ready()
	ui.output()

	#game start
	ui.gaming()
	ui.output()

	#b's turn
	ui.changeTurn('B')
	ui.output()

	#b post 999, c's turn
	ui.changePlayerContent('B', '999')
	ui.changeTurn('C')
	ui.output()

	#game finish
	ui.wait()
	ui.output()
	print ''
