import gameUtils

class Player:

	name = ''

	isReady = False

	isTurn = False

	def __init__(self, name):
		self.name = name

class Game:

	playerId = 0

	isStart = False

	players = []

	leftCards = []

	postedCards = []

	def addPlayer(self, name):
		for player in self.players:
			if player.name == name:
				return False
		self.players.append(Player(name))
		self.playerId = self.playerId + 1
		return True

	def delPlayer(self, name):
		pos = 0
		for player in self.players:
			if player.name == name:
				break
			pos = pos + 1
		if pos != len(self.players):
			self.players.pop(pos)

	def getPlayer(self, name):
		for player in self.players:
			if player.name == name:
				return player
		return None

	def getId(self):
		return self.playerId

	def initCards(self):
		self.leftCards = []
		for i in range(4):
			for j in range(13):
				self.leftCards.append(j + 1)
		self.leftCards.append(14)
		self.leftCards.append(15)