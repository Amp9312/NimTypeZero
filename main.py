# Dev - Amp
# Project - Nim Type Zero
# Last Modified 1/12/2021

# GLOBAL ASS VARIABLES - SIN DO NOT COMMIT THIS HERESY LATER

cardTag1 = "Spades"
cardTag2 = "Hearts"
cardTag3 = "Diamonds"
cardTag4 = "Clubs"

version = "1.0"

# IMPORTS

import random



# CLASSES

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def show(self):
        print("{} of {}".format(self.value, self.suit))


# BIG ASS DECK CLASS FOR ALL YOUR DECK NEEDS AND DECK ACCESSORIES
class Deck:
    def __init__(self):
        self.cards = []
        self.build(cardTag1, cardTag2, cardTag3, cardTag4)

    # What do you think this does?
    def build(self, cardType1, cardType2, cardType3, cardType4):
        for s in [cardType1, cardType2, cardType3, cardType4]:
            for v in range(0, 4):
                self.cards.append(Card(s, v))

    # This is a debug method that shows me the deck
    def show(self):
        for c in self.cards:
            c.show()

    # Uses psuedorandom shenanigans to let me rearrange the cards in the stack
    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    #draws exactly one card from the stack (deck). This can be done until the deck is gone (not recommended)
    def drawOneCard(self):
        return self.cards.pop()

# HOLD ON TO YOUR SEATS BOYZ ITS A FUCKIN PLAYER CLASS *AIR HORNS*
class Player:
    def __init__(self, name):
        # This uniquely identifies the player
        self.name = name
        # This is an array that contains the players hand - is unique to their object
        self.hand = []

    # method that allows one player to draw all four cards for their hand at once
    # technically not legal in actual casino play but it's all random who cares
    # what am I expected to do have each object call this method once in sequence four times? Get outta here
    def draw(self, deck):
        for _ in range(4):
            self.hand.append(deck.drawOneCard())

        return self

    # Debug tool that shows me what a player's hand contains
    def revealHand(self):
        print(" ")
        print("This is " + self.name + 's Hand:')

        # this is definitely some woo woo magic I actually didn't expect this to work
        for card in self.hand:
            card.show()

    # Debug tool that may actually get used later to pull player names in game
    def whatIsName(self):
        return self.name



# FUNCTIONS
def initiate(player1, player2, player3, player4):


    # test = Card("Hearts", 0)          Debugging card object
    # test.show()                       Displaying the debugging
    # Creating the actual Deck
    testDeck = Deck()
    # Shuffling that bad boy
    testDeck.shuffle()
    # testDeck.show()                   Shows all the cards in the deck for debugging purposes
    # card = testDeck.drawOneCard()     Pop the top card of the deck for debugging purposes (volatile)
    # card.show()                       Shows the card popped (volatile)

    # Creates player object
    player = Player(player1)

    # Instantiate rest of players for testing purposes
    bot1 = Player(player2)
    bot2 = Player(player3)
    bot3 = Player(player4)


    print('Hello! Welcome to Nim Type Zero ' + player.whatIsName())
    print('Ver: ' + version + '\n')

    # Players draw their hands
    # Note - because cards are being pulled from the stack if you make each player draw 11 instead of 4
    # the deck WILL run out by the time it gets to player 4
    player.draw(testDeck)
    bot1.draw(testDeck)
    bot2.draw(testDeck)
    bot3.draw(testDeck)

    # Show hand for debugging purposes
    player.revealHand()
    bot1.revealHand()
    bot2.revealHand()
    bot3.revealHand()

# Retrieving player name via input
player1 = input('Hello! What is your name?\r\n')

# Creating more player names for testing purposes
player2 = "Bob"
player3 = "Tom"
player4 = "Sam"

# This is where "main" or the "actual code" begins

initiate(player1, player2, player3, player4)
