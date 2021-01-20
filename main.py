# Dev - Amp
# Project - Nim Type Zero
# Last Modified 1/19/2021

# TODO
# Add getter methods as more propertiees in the player object are made
# Implement betting logic

# GLOBAL ASS VARIABLES - SIN DO NOT COMMIT THIS HERESY LATER

CARDTAGS = ["Spades", "Hearts", "Diamonds", "Clubs"]

VERSION = "2.0"

# IMPORTS

import random
from os import linesep as os_linesep


# CLASSES

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def __str__(self):
        return "{} of {}".format(self.value, self.suit)


class Deck:
    def __init__(self):
        self.cards = []
        for s in CARDTAGS:
            for v in range(0, 4):
                self.cards.append(Card(s, v))

    def __str__(self):
        result = ""
        for c in self.cards:
            result += str(c) + os_linesep
        return result

    # Uses psuedo random shenanigans to rearrange the cards in the stack
    def shuffle(self):
        random.shuffle(self.cards)

    # draws exactly one card from the stack (deck). This can be done until the deck is gone (not recommended)
    def drawOneCard(self):
        return self.cards.pop()


class Player:
    def __init__(self, name, isHuman=False):
        self.name = name  # This uniquely identifies the player
        self.isHuman = isHuman  # This tells us if the player object is playable
        self.hand = []  # This is an array that contains the players hand - is unique to their object

    def __str__(self):
        # nasty one liner: str.join, and list comprehension
        # list comprehensions are your friend. Trust me.
        return os_linesep + "This is " + self.name + 's Hand:' + os_linesep + os_linesep.join(
            [str(x) for x in self.hand])

    def draw(self, deck, numCards):  # method that allows one player to draw all four cards for their hand at once
        for _ in range(numCards):
            self.hand.append(deck.drawOneCard())

    # Debug tool that may actually get used later to pull player names in game
    def whatIsName(self):
        return self.name

    def whatIsStatus(self):
        return str(self.isHuman)


# FUNCTIONS

def bettingPhase():
    print("{0}Betting Options: {0} 1.) Fold {0} 2.) Raise {0} 3.) Call".format(os_linesep))
    playerChoice = input("Which do you choose? {}".format(os_linesep))

    # Implement betting Logic later


def initiate(players):
    # test = Card("Hearts", 0)          Debugging card object
    # print(test)                       Displaying the debugging

    # Creating the actual Deck
    testDeck = Deck()

    # Shuffling that bad boy
    testDeck.shuffle()

    # show me the shuffled deck
    # print(testDeck)

    # show me that the player list is shuffled
    # print(players[1])

    # card = testDeck.drawOneCard()     Pop the top card of the deck for debugging purposes (volatile)
    # card.show()                       Shows the card popped (volatile)

    # draw players test hands
    for player in players:
        player.draw(testDeck, 4)

    # print players test hands
    # for player in players:
    #    print(player)

    print('Hello! Welcome to Nim Type Zero ' + players[0].whatIsName())

    # Reminder for later: os_linesep logic adds the VERSION global
    # variable to sub for the first {}, and then a newline for the second {}
    print('Ver: {}{}'.format(VERSION, os_linesep))

    print(players[0])

    bettingPhase()

    # randomize turn order
    # random.shuffle(players)

    # Betting Phase
    # bettingPhase()


# This is where the "main" code begins

player1 = input('Hello! What is your name?{}'.format(os_linesep))

# Creating more player names for testing purposes
nameList = [player1, "Bob", "Tom", "Sam"]

# Creates a list of player objects based on the names pulled from nameList
playerList = [Player(x) for x in nameList]

initiate(playerList)
