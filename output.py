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
        for card in player.cards:
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