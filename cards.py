import random

# Card class
class Card(object):
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
class Deck(object):
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