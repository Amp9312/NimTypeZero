# Dev - Amp
# Project - Nim Type Zero
# Last Modified 1/12/2021

cardTags = ["Spades", "Hearts", "Diamonds", "Clubs"]  # making this a list cleans up a lot of things

version = "1.0"

import random
from os import linesep as os_linesep


class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def __str__(self):
        return "{} of {}".format(self.value, self.suit)


class Deck:
    def __init__(self):
        self.cards = []
        for s in cardTags:
            for v in range(0, 4):
                self.cards.append(Card(s, v))

    def __str__(self):
        result = ""
        for c in self.cards:
            result += c + os_linesep
        return result

    def shuffle(self):
        random.shuffle(self.cards)

    def drawOneCard(self):
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def __str__(self):
        # nasty one liner: str.join, and list comprehension
        # list comprehensions are your friend. Trust me.
        return os_linesep + "This is " + self.name + 's Hand:' + os_linesep + os_linesep.join([str(x) for x in self.hand])

    def draw(self, deck, numCards):
        for _ in range(numCards):
            self.hand.append(deck.drawOneCard())

    # Debug tool that may actually get used later to pull player names in game
    def whatIsName(self):
        return self.name



def init(players):
    # test = Card("Hearts", 0)          Debugging card object
    # test.show()                       Displaying the debugging
    testDeck = Deck()
    testDeck.shuffle()
    # testDeck.show()                   Shows all the cards in the deck for debugging purposes
    # card = testDeck.drawOneCard()     Pop the top card of the deck for debugging purposes (volatile)
    # card.show()                       Shows the card popped (volatile)

    print('Hello! Welcome to Nim Type Zero ' + players[0].whatIsName())
    print('Ver: ' + version + '\n')

    
    # Players draw their hands
    # Note - because cards are being pulled from the stack if you make each player draw 11 instead of 4
    # the deck WILL run out by the time it gets to player 4
    for player in players:
        player.draw(testDeck, 4)

    # Show hand for debugging purposes
    for player in players:
        print(player)


player1 = input('Hello! What is your name?'+os_linesep)
nameList = [player1, "Bob", "Tom", "Sam"]
playerList = [Player(x) for x in nameList]  # list comprehension, short hand for generating a list in a loop
init(playerList)
