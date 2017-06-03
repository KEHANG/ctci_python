import random
import unittest

class Suit(object):

	def __init__(self, suitType):

		if suitType in ['Club', 'Diamond', 'Heart', 'Spade']:
			self.suitType = suitType
		else:
			raise Exception('Unable to recognize suit type: {0}'.format(suitType))

class Card(object):

	def __init__(self, suit, faceValue):

		self.suit = suit
		self.faceValue = faceValue

	def getFaceValue(self):

		return self.faceValue

	def isAce(self):
		if self.faceValue == 1:
			return True
		else:
			return False

class BlackJackCard(Card):

	def __init__(self, suit, faceValue):
		super(BlackJackCard, self).__init__(suit, faceValue)

	def getMinValue(self):
		if self.isAce():
			return 1
		else:
			return self.faceValue

	def getMaxValue(self):
		if self.isAce():
			return 11
		else:
			return self.faceValue
		

class Deck(object):

	def __init__(self, cards):
		self.cards = cards

	def shuffle(self, seed=None):
		if not seed:
			random.shuffle(self.cards)

	def remainingCards(self):
		return len(self.cards)

	def dealCard(self):
		return self.cards.pop(0)

class Hand(object):

	def __init__(self, cards):
		self.cards = cards

	def score(self):

		value = 0
		for card in self.cards:
			value += card.getFaceValue()

		return value

	def receiveCard(self, card):
		self.cards.append(card)

class BlackJackHand(Hand):

	def __init__(self, cards):
		super(BlackJackHand, self).__init__(cards)

	def getPossibleScores(self, cards):
		
		if len(cards) == 0:
			return []
		elif len(cards) == 1:
			card = cards[0]
			return [card.getMinValue(), card.getMaxValue()]
		else:
			card = cards[0]
			scoresOfOtherCards = self.getPossibleScores(cards[1:])
			lowScores = [card.getMinValue() + score for score in scoresOfOtherCards]
			highScores = [card.getMaxValue() + score for score in scoresOfOtherCards]
			return lowScores + highScores

	def getUniquePossibleScores(self):

		possibleScores = self.getPossibleScores(self.cards)
		uniquePossibleScores = []
		for possibleScore in possibleScores:
			if possibleScore not in uniquePossibleScores:
				uniquePossibleScores.append(possibleScore)

		return uniquePossibleScores

	def score(self):

		possibleScores = self.getUniquePossibleScores()

		if 21 in possibleScores:
			return 21

		sortedScores = sorted(possibleScores, 
							key=lambda score: (abs(score-21)/(score-21),abs(score-21)))

		return sortedScores[0]


class TestBlackJackHand(unittest.TestCase):

	def test_score1(self):
		faceValues = [1, 3, 5, 7, 11, 4]
		suit = Suit('Spade')
		cards = [BlackJackCard(suit, faceValue) for faceValue in faceValues]
		blackJackHand = BlackJackHand(cards)

		expectedPossibleUniqueScores = [31, 41]
		self.assertEqual(expectedPossibleUniqueScores, 
						sorted(blackJackHand.getUniquePossibleScores()))

		expectedScore = 31
		self.assertEqual(expectedScore, blackJackHand.score())

	def test_score2(self):
		faceValues = [1, 1, 5, 7]
		suit = Suit('Spade')
		cards = [BlackJackCard(suit, faceValue) for faceValue in faceValues]
		blackJackHand = BlackJackHand(cards)

		expectedPossibleUniqueScores = [14, 24, 34]
		self.assertEqual(expectedPossibleUniqueScores, 
						sorted(blackJackHand.getUniquePossibleScores()))

		expectedScore = 14
		self.assertEqual(expectedScore, blackJackHand.score())

	def test_score3(self):
		faceValues = [1, 1, 2, 7]
		suit = Suit('Spade')
		cards = [BlackJackCard(suit, faceValue) for faceValue in faceValues]
		blackJackHand = BlackJackHand(cards)

		expectedPossibleUniqueScores = [11, 21, 31]
		self.assertEqual(expectedPossibleUniqueScores, 
						sorted(blackJackHand.getUniquePossibleScores()))

		expectedScore = 21
		self.assertEqual(expectedScore, blackJackHand.score())

	def test_score4(self):
		faceValues = [1, 1, 2, 5]
		suit = Suit('Spade')
		cards = [BlackJackCard(suit, faceValue) for faceValue in faceValues]
		blackJackHand = BlackJackHand(cards)

		expectedPossibleUniqueScores = [9, 19, 29]
		self.assertEqual(expectedPossibleUniqueScores, 
						sorted(blackJackHand.getUniquePossibleScores()))

		expectedScore = 19
		self.assertEqual(expectedScore, blackJackHand.score())

