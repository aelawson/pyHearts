import random
import time
import pdb

# Card class
class Card():
	def __init__(self, suit, value):
		self.owner = None
		self.suit = suit
		self.value = value
	def getSuit(self):
		return self.suit
	def getValue(self):
		return self.value
	def getOwner(self):
		return self.owner
	def setOwner(self, owner):
		self.owner = owner

# Deck class
class Deck():
	def __init__(self, cards):
		self.cards = cards
	# Shuffles the deck
	def shuffle(self):
		random.shuffle(self.cards)
	# Checks if the deck is empty
	def isEmpty(self):
		if len(self.cards) is 0:
			return True
		else:
			return False
	# Play the next card
	def dealCard(self):
		return self.cards.pop()
	# Returns the list of cards in the deck
	def getCards(self):
		return self.cards

# Player class
class Player():
	def __init__(self, name, points):
		self.name = name
		self.cards = []
		self.points = points
	def getName(self):
		return self.name
	def getCards(self):
		return self.cards
	def addCard(self, card):
		self.cards.append(card)
	def removeCard(self, card):
		for x in self.cards:
			if x.getValue() is card.getValue() and x.getSuit() is card.getSuit():
				self.cards.remove(x)
				break
	def addPoints(self, points):
		self.points += points
	def getPoints(self):
		return self.points
	def setNextPlayer(self, nextPlayer):
		self.nextPlayer = nextPlayer
	def getNextPlayer(self):
		return self.nextPlayer
	def sortHand(self):
		spades = []
		diamonds = []
		hearts = []
		clubs = []
		for card in self.cards:
			if card.getSuit() is 'C':
				clubs.append(card)
			elif card.getSuit() is 'H':
				hearts.append(card)
			elif card.getSuit() is 'D':
				diamonds.append(card)
			elif card.getSuit() is 'S':
				spades.append(card)
		clubs.sort()
		hearts.sort()
		diamonds.sort()
		spades.sort()
		self.cards = clubs
		self.cards.extend(hearts)
		self.cards.extend(diamonds)
		self.cards.extend(spades)
	def playCard(self):
		return self.cards.pop()

# Computer class
#class Computer(player):
	#player.__init__(self)

# Check each player's score.
def checkScore(player, dealer):
    # Check player's score
    if player.getPoints() >= 50:
        return True
    # Tail case
    if player.getNextPlayer() is dealer:
        return False
    # Recursively check scores
    else:
        checkScore(player.getNextPlayer(), dealer)

# Print each player's score.
def printScore(player, dealer):
	# Print player's score
    print str(player.getName()) + "`s current score is: " + str(player.getPoints()) + " points."
	# Tail case
    if player.getNextPlayer() is dealer:
        print "\n"
        return
    # Recursively print scores
    else:
        printScore(player.getNextPlayer(), dealer)

# Print the player's hand
def printHand(player):
    # Base case
    if player.getName() is 'Player':
        print "YOUR HAND:"
        for card in human.getCards():
            print '|' + str(card.getValue()) + ' ' + str(card.getSuit()) + '|',
        print "\n"
        return
    # Recursively find player
    else:
        printHand(player.getNextPlayer())

# Print the table
def printTable(table):
	print "THE TABLE:"
	for card in table:
		print '|' + str(card.getValue()) + ' ' + str(card.getSuit()) + '|',
	print "\n"

# Deal the deck
def deal(deck, player):
	# Base case
	if deck.isEmpty() is True:
		return
	# Recursively deal around the table
	else:
		card = deck.dealCard()
		card.setOwner(player)
		player.addCard(card)
		deal(deck, player.getNextPlayer())

# Make a move around the table
def makeMove(table, player, trump):
	# Base case
    if len(table) is 4:
        pass
    # Recursively play around the table
    elif player.getName() is 'Player':
        # Receive card choice from player in format Value, Suit
        card = str(raw_input("Choose a card to play (V,S): "))
        print "\n"
        value, suit = card.split(",")
        # Search through players cards
        # CHANGE: Binary search. Response if card is not there. Must follow trump.
        # CHANGE: Cannot open with hearts or QoS.
        for card in player.getCards():
        	if int(value) is card.getValue() and suit is card.getSuit():
            	# If first move, define the round trump
    			if len(table) is 0:
    			    trump = card.getSuit()
    			# Add move to table
    			table.append(card)
    			# Remove from player's hand
    			player.removeCard(card)
    			printTable(table)
    			break
        table, trump = makeMove(table, player.getNextPlayer(), trump)
    else:
		# Computer is pseudo-thinking...
        time.sleep(1)
        card = player.playCard()
		# If first move, define the round trump
        if len(table) is 0:
            trump = card.getSuit()
		# Add card to table
        table.append(card)
		# Remove from player's hand
        player.removeCard(card)
        printTable(table)
        table, trump = makeMove(table, player.getNextPlayer(), trump)
	# Return the table and round trump
    return table, trump

# Calculate the points from the hand
def calculatePoints(table, discards, trump):
    bestCard = None
    totalPoints = 0
    # Find the trump card and determine point payout
    for card in table:
    	# Condition for Queen of Spades
    	if card.getSuit() is 'S' and card.getValue() is '12':
    		totalPoints += 13
    	# Condition for Hearts
    	elif card.getSuit() is 'H':
    		totalPoints += 1
    	# Condition for trump suit
    	if card.getSuit() is trump:
    		if bestCard is None or card.getValue() > bestCard.getValue():
    			bestCard = card
    # Announce winner
    time.sleep(1)
    print str(bestCard.getOwner().getName()) + " takes the hand...\n"
    time.sleep(1)
    # Give points to trump card owner
    bestCard.getOwner().addPoints(totalPoints)
    # Return empty table and discards
    return [], discards.extend(table)

# Play the game
def playGame(table, discards, deck, dealer):
    # Base case
    if checkScore(dealer, dealer):
       return
    # Recursively plays the game
    else:
        # Deal and start game
        print "Dealing the deck...\n"
        time.sleep(2)
        deck.shuffle()
        deal(deck, dealer.getNextPlayer())
        # Play 13 rounds (one for each card)
        for round in range(13):
            # Round schedule
            printHand(dealer)
            table, trump = makeMove(table, dealer.getNextPlayer(), None)
            table, discards = calculatePoints(table, discards, trump)
            printScore(dealer, dealer)
        # Reshuffle the deck
        deck = Deck(discards)
        deck.shuffle()
        deal(deck, dealer.getNextPlayer())
        playGame(table, discards, deck, dealer.getNextPlayer())

# Welcome message
print "------------------"
print "WELCOME TO HEARTS!"
print "By: Andrew Lawson"
print "------------------"
time.sleep(2)
# Initialize table
table = []
discards = []
# Initialize players
human = Player('Player', 0)
cpuOne = Player('CPU1', 0)
cpuTwo = Player('CPU2', 0)
cpuThree = Player('CPU3', 0)
human.setNextPlayer(cpuOne)
cpuOne.setNextPlayer(cpuTwo)
cpuTwo.setNextPlayer(cpuThree)
cpuThree.setNextPlayer(human)
# Intialize deck
cards = []
for suit in ['C', 'H', 'D', 'S']:
	for value in range(2, 15):
		card = Card(suit, value)
		cards.append(card)
deck = Deck(cards)
playGame(table, discards, deck, human)