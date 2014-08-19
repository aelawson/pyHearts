# Player class
class Player(object):
    def __init__(self, name, points):
        self._name = name
        self._next_player = None
        self._spades = []
        self._diamonds = []
        self._hearts = []
        self._clubs = []
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
        # Separate cards into suit lists
        for card in self._cards:
            if card.suit is 'C':
                self._clubs.append(card)
            elif card.suit is 'H':
                self._hearts.append(card)
            elif card.suit is 'D':
                self._diamonds.append(card)
            elif card.suit is 'S':
                self._spades.append(card)
        # Sort each suit
        self._clubs.sort(key = lambda x: x.value, reverse = False)
        self._hearts.sort(key = lambda x: x.value, reverse = False)
        self._diamonds.sort(key = lambda x: x.value, reverse = False)
        self._spades.sort(key = lambda x: x.value, reverse = False)
        # Create a singular list of cards, clubs to spades.
        self._cards = self._clubs
        self._cards.extend(self._hearts)
        self._cards.extend(self._diamonds)
        self._cards.extend(self._spades)
    def play_card(self):
        return self._cards.pop()

# Human class
class Human(Player):
    def __init__(self, name, points):
        Player.__init__(self, name, points)

# Computer class
class Computer(Player):
    def __init__(self, name, points):
        Player.__init__(self, name, points)
    def play_card(self, table, trump, broken, roundNum):
        # If it's the first round
        if roundNum is 0:
            # If it's the first card (opening card)
            if len(table) is 0:
                for card in self._cards:
                    # Must play 2 of Clubs
                    if card.suit is 'C' and card.value is 2:
                        return card
            # If it's not the first card
            if len(table) is not 0:
                trumpCards = []
                otherCards = []
                # Find the highest table card in the trump suit
                maxCard = None
                for card in table:
                    if card.suit is trump:
                        trumpCards.append(card)
                    else:
                        otherCards.append(card)
                # Return the highest player card within trump suit
                for card in trumpCards:
                    if maxCard is None or card.value > maxCard.value:
                        maxCard = card
                if trump is 'S':
                    for card in self._spades:
                        if maxCard is None or card.value > maxCard.value:
                            maxCard = card
                elif trump is 'D':
                    for card in self._diamonds:
                        if maxCard is None or card.value > maxCard.value:
                            maxCard = card
                elif trump is 'H':
                    for card in self._hearts:
                        if maxCard is None or card.value > maxCard.value:
                            maxCard = card
                elif trump is 'C':
                    for card in self._spades:
                        if maxCard is None or card.value > maxCard.value:
                            maxCard = card
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