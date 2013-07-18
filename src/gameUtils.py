

cards = [(1, 'A'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), 
		(6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '0'),
		(11, 'J'),(12, 'Q'),(13, 'K'),(14, 'N'),(15, 'M'),]

def spliteCards(cards):
	#cards is string mult cards
	intCards = []
	for card in cards:
		if isCardValid(card):
			intCards.append(atoi(card))
	return intCards.sort()

def isCardValid(strCard):
	#check single card
	if len(strCard) != 1:
		return False

	for card in cards:
		intC, strC = card
		if strCard == strC:
			return True
	return False

def itoa(intCard):
	#change int value card to string card
	for card in cards:
		intC, strC = card
		if intC == intCard:
			return strC
	return ''

def atoi(strCard):
	#change string card to int value card
	for card in cards:
		intC, strC = card
		if strC == strCard:
			return intC
	return -1