import random
import time
import pdb

# Card class
class Card():
	def __init__(self, suit, value):
		self._owner = None
		self._suit = suit
		self._value = value
	@property
	def suit(self):
		return self._suit
	@property
	def value(self):
		return self._value
	@property
	def owner(self):
		return self._owner
	@owner.setter
	def owner(self, owner):
		self._owner = owner

# Deck class
class Deck():
	def __init__(self, cards):
		self._cards = cards
	@property
	def empty(self):
		if len(self._cards) is 0:
			return True
		else:
			return False
	@property
	def cards(self):
		return self._cards
	def deal_card(self):
		return self._cards.pop()
	def shuffle(self):
		random.shuffle(self._cards)

# Player class
class Player():
	def __init__(self, name, points):
		self._name = name
		self._next_player = None
		self._cards = []
		self._points = points
	@property
	def name(self):
		return self._name
	@property
	def cards(self):
		return self._cards
	@property
	def points(self):
		return self._points
	@property
	def next_player(self):
		return self._next_player
	@next_player.setter
	def next_player(self, nextPlayer):
		self._next_player = nextPlayer
	def add_card(self, card):
		self._cards.append(card)
	def remove_card(self, card):
		for x in self.cards:
			if x.value is card.value and x.suit is card.suit:
				self.cards.remove(x)
				break
	def add_points(self, points):
		self._points += points
	def sort_hand(self):
		_spades = []
		_diamonds = []
		_hearts = []
		_clubs = []
		for card in self._cards:
			if card.suit is 'C':
				_clubs.append(card)
			elif card.suit is 'H':
				_hearts.append(card)
			elif card.suit is 'D':
				_diamonds.append(card)
			elif card.suit is 'S':
				_spades.append(card)
		_clubs.sort()
		_hearts.sort()
		_diamonds.sort()
		_spades.sort()
		self._cards = _clubs
		self._cards.extend(_hearts)
		self._cards.extend(_diamonds)
		self._cards.extend(_spades)
	def play_card(self):
		return self._cards.pop()

# Computer class
#class Computer(player):
	#player.__init__(self)

# Check each player's score.
def check_score(player, dealer):
    if player.points >= 50:
        return True
    if player.next_player is dealer:
        return False
    # Recursively check scores
    else:
        check_score(player.next_player, dealer)

# Print each player's score.
def print_score(player, dealer):
    print str(player.name) + "`s current score is: " + str(player.points) + " points."
    if player.next_player is dealer:
        print "\n"
        return
    # Recursively print scores
    else:
        print_score(player.next_player, dealer)

# Print the player's hand
def print_hand(player):
    if player.name is 'Player':
        print "YOUR HAND:"
        for card in human.cards:
            print '|' + str(card.value) + ' ' + str(card.suit) + '|',
        print "\n"
        return
    # Recursively find player
    else:
        print_hand(player.next_player)

# Print the table
def print_table(table):
	print "THE TABLE:"
	for card in table:
		print '|' + str(card.value) + ' ' + str(card.suit) + '|',
	print "\n"

# Deal the deck
def deal(deck, player):
	if deck.empty is True:
		return
	# Recursively deal around the table
	else:
		card = deck.deal_card()
		card.owner = player
		player.add_card(card)
		deal(deck, player.next_player)

# Make a move around the table
def make_move(table, player, trump):
    if len(table) is not 4:
	    # Recursively play around the table
	    if player.name is 'Player':
	        # Receive card choice from player in format Value, Suit
	        card = str(raw_input("Choose a card to play (V,S): "))
	        print "\n"
	        value, suit = card.split(",")
	        # Search through players cards
	        # CHANGE: Binary search. Response if card is not there. Must follow trump.
	        # CHANGE: Cannot open with hearts or QoS.
	        for card in player.cards:
	        	if int(value) is card.value and suit is card.suit:
	            		# If first move, define the round trump
	    			if len(table) is 0:
	    			    trump = card.suit
	    			# Add move to table
	    			table.append(card)
	    			# Remove from player's hand
	    			player.remove_card(card)
	    			print_table(table)
	    			break
	        table, trump = make_move(table, player.next_player, trump)
	    else:
		# Computer is pseudo-thinking...
	        time.sleep(1)
	        card = player.play_card()
		# If first move, define the round trump
	        if len(table) is 0:
	            trump = card.suit
		# Add card to table
	        table.append(card)
		# Remove from player's hand
	        player.remove_card(card)
	        print_table(table)
	        table, trump = make_move(table, player.next_player, trump)
    return table, trump

# Calculate the points from the hand
def calculate_points(table, discards, trump):
    bestCard = None
    totalPoints = 0
    # Find the trump card and determine point payout
    for card in table:
    	# Condition for Queen of Spades
    	if card.suit is 'S' and card.value is '12':
    		totalPoints += 13
    	# Condition for Hearts
    	elif card.suit is 'H':
    		totalPoints += 1
    	# Condition for trump suit
    	if card.suit is trump:
    		if bestCard is None or card.value > bestCard.value:
    			bestCard = card
    # Announce winner
    time.sleep(1)
    print str(bestCard.owner.name) + " takes the hand...\n"
    time.sleep(1)
    # Give points to trump card owner
    bestCard.owner.add_points(totalPoints)
    # Return empty table and discards
    return [], discards.extend(table)

# Play the game
def play_game(table, discards, deck, dealer):
    # Base case
    if check_score(dealer, dealer):
       return
    # Recursively plays the game
    else:
        # Deal and start game
        print "Dealing the deck...\n"
        time.sleep(2)
        deck.shuffle()
        deal(deck, dealer.next_player)
        # Play 13 rounds (one for each card)
        for round in range(13):
            # Round schedule
            print_hand(dealer)
            table, trump = make_move(table, dealer.next_player, None)
            table, discards = calculate_points(table, discards, trump)
            print_score(dealer, dealer)
        # Reshuffle the deck
        deck = Deck(discards)
        deck.shuffle()
        deal(deck, dealer.next_player)
        play_game(table, discards, deck, dealer.next_player)

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
human.next_player = cpuOne
cpuOne.next_player = cpuTwo
cpuTwo.next_player = cpuThree
cpuThree.next_player = human
# Intialize deck
cards = []
for suit in ['C', 'H', 'D', 'S']:
	for value in range(2, 15):
		card = Card(suit, value)
		cards.append(card)
deck = Deck(cards)
play_game(table, discards, deck, human)
