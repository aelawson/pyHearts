import time

from output import print_hand, print_table, print_score
from cards import Card, Deck
from players import Player

# Find 2 of Clubs
def find_starter(player):
    for card in player.cards:
        if card.value is 2 and card.suit is 'C':
            return player
    return find_starter(player.next_player)

# Check each player's score.
def check_score(player, dealer):
    if player.points >= 50:
        return True
    if player.next_player is dealer:
        return False
    # Recursively check scores
    else:
        check_score(player.next_player, dealer)

# See if a player's move was valid and if hearts are broken.
def check_move(value, suit, table, player, trump, broken, roundNum):
    # If it's the first round
    if roundNum is 0:
        # If it's the first card
        if len(table) is 0:
            if suit is not 'C' and value is not 2:
                print "You must lead with the 2 of Clubs.\n"
                return broken, False
            else:
                return broken, True
        # If it's not the first card
        elif len(table) is not 0:
            if suit is not trump:
                for c in player.cards:
                    if c.suit is trump:
                        print "You must follow the trump suit.\n"
                        return broken, False
            elif suit is 'H' or (suit is 'S' and value is 12):
                print "Cannot break hearts on first hand.\n"
                return broken, False
            else:
                return broken, True
    # If it's not the first round
    elif roundNum is not 0:
        # If the Queen of Spades is played
        if (suit is 'S' and value is '12') and broken is False:
            broken = True
        # If it's the first card
        if len(table) is 0:
            if suit is 'H' and broken is False:
                print "Hearts are not broken yet.\n"
                return broken, False
            else:
                return broken, True
        # If it's not the first card
        elif len(table) is not 0:
            if suit is not trump:
                for c in player.cards:
                    if c.suit is trump:
                        print "You must follow the trump suit.\n"
                        return broken, False
            else:
                return broken, True
            if suit is 'H' and broken is False:
                broken = True

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

# Make moves around the table
def make_move(table, player, trump, broken, roundNum):
    if len(table) is not 4:
        # Recursively play around the table
        if player.name is 'Player':
            # Receive card choice from player in format Value, Suit
            # If the player does not play a valid move, requery them.
            validMove = False
            while validMove is False:
                card = str(raw_input("Choose a card to play (V,S): "))
                value, suit = card.split(",")
                broken, validMove = check_move(value, suit, table, player, trump, broken, roundNum)
            print "\n"
            # Search through players cards
            # CHANGE: Binary search?
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
            table, trump = make_move(table, player.next_player, trump, broken, roundNum)
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
            table, trump = make_move(table, player.next_player, trump, broken, roundNum)
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
    discards.extend(table)
    return [], discards

# Play the game
def play_game(table, discards, deck, dealer):
    global human
    if check_score(dealer, dealer):
       return
    # Recursively plays the game
    else:
        print "Dealing the deck...\n"
        time.sleep(2)
        deck.shuffle()
        deal(deck, dealer.next_player)
        human.sort_hand()
        starter = find_starter(dealer)
        # Play 13 rounds (one for each card)
        for roundNum in range(13):
            # Round schedule
            print_hand(starter)
            table, trump = make_move(table, starter, None, False, roundNum)
            table, discards = calculate_points(table, discards, trump)
            print_score(starter, starter)
        # Reshuffle the deck
        deck = Deck(discards)
        deck.shuffle()
        deal(deck, starter.next_player)
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
# Temporary global var (will remove)
global human
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