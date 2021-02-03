# Dev - Amp
# Project - Nim Type Zero
# Last Modified 2/2/2021

# TODO
# Add getter methods as more properties in the player object are made
# Implement betting logic

# GLOBAL ASS VARIABLES - SIN DO NOT COMMIT THIS HERESY LATER

CARDTAGS = ["Spades", "Hearts", "Diamonds", "Clubs"]

VERSION = "3.0"

POT = 0

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
    def __init__(self, name, isHuman = False, money=50, status = ""):
        self.money = money
        self.status = status
        self.name = name  # This uniquely identifies the player
        self.isHuman = isHuman  # This tells us if the player object is playable
        self.hand = []  # This is an array that contains the players hand - is unique to their object

    def __str__(self):
        # nasty one liner: str.join, and list comprehension
        # list comprehensions are your friend. Trust me.
        return os_linesep + "This is " + self.name + "'s Hand:" + os_linesep + os_linesep.join([str(x) for x in self.hand]) + os_linesep + self.name + 's Amoney: ' + str(self.money)

    def draw(self, deck, numCards):  # method that allows one player to draw all four cards for their hand at once
        for _ in range(numCards):
            self.hand.append(deck.drawOneCard())

    # Debug tool that may actually get used later to pull player names in game
    def whatIsName(self):
        return self.name

    def isHuman(self):
        return str(self.isHuman)

    def checkMoney(self):
        return self.money

    def subMoney(self, betAmount):
        self.money = self.money - betAmount

    def fold(self):
        self.status = "Fold"

    def setStatus(self, status):
        self.status = status

    def checkStatus(self):
        return self.status




# FUNCTIONS
def isOpen():
    if(POT == 0):
        return True

def addPot(betAmount):
    global POT
    POT += betAmount


def bettingPhase(players):
    global POT
    ## This logic determines if a player is the first to open or not
    if(isOpen()):
        print("{0}Betting Options: {0} 1.) Open {0} 2.) Fold".format(os_linesep))
        openChoice = input("Which do you choose?{}".format(os_linesep))
        openChoice = int(openChoice)
        ## userInput = 1
        if(openChoice == 1):
            print("You have chosen to open. How much are you opening with?")
            openingAmount = input("Enter an amount to open with: ".format(os_linesep))
            openingAmount = int(openingAmount)
            strOpeningAmount = str(openingAmount)
            if(openingAmount <= 0):
                print("You cannot open with nothing.")
                bettingPhase(players)
            elif(openingAmount > players.checkMoney()):
                print("To open the amount of: " + strOpeningAmount + " you need more money. Try betting lower{}".format(os_linesep))
                bettingPhase(players)
            else:
                print("You have chosen to Open with: " + strOpeningAmount + "{}".format(os_linesep))
                players.subMoney(openingAmount)
                addPot(openingAmount)
                print("Money left: " + str(players.checkMoney()) + " Pot: " + str(POT) + " {}".format(os_linesep))
                ## userInput = 1
        elif(openChoice == 2):
            print("You have chosen to fold. You will not be participating this round.")
            players.fold()
        else:
            print("Not a Valid Input. Try again.")
            bettingPhase(players)

    ## The player is not the first to open
    else:
        print("{0}Betting Options: {0} 1.) Fold {0} 2.) Raise {0} 3.) Call".format(os_linesep))
        playerChoice = input("Which do you choose? {}".format(os_linesep))
        if(playerChoice == "1"):
            print("You chosen to fold, you will not play this round{}".format(os_linesep))
            players.fold()
        elif(playerChoice == "2"):
            print("You have chosen to Raise, what are you betting?")
            bettingAmount = input("Enter an amount higher than the current pot: " + str(POT) + "{}".format(os_linesep))
            inputPlayerChoice = int(bettingAmount)
            if(inputPlayerChoice < POT):
                print("To Raise you must bet more than current pot: " + str(POT) + "{}".format(os_linesep))
                bettingPhase(players)
            elif(inputPlayerChoice > players.checkMoney()):
                print("To Raise the amount of: '" + str(bettingAmount) + "' You need more than " + str(players.checkMoney()) + " money{0}".format(os_linesep))
                bettingPhase(players)
            else:
                print("You have chosen to Raise: " + bettingAmount + "{}".format(os_linesep))
                players.subMoney(inputPlayerChoice)
                addPot(inputPlayerChoice)
                print("Current Money is: " + str(players.checkMoney()) + " Current Pot is: " + str(POT))
        elif(playerChoice == "3"):
            print("You have chosen to Call, you are matching the current open of: " + str(POT))
            inputPlayerConfirm = input("To confirm your call, type yes or no (Y/N)".format(os_linesep))
            if(inputPlayerConfirm == "Y"):
                players.subMoney(POT)
                addPot(POT)
                print("Current Money: " + str(players.checkMoney()))
                print("Current Pot: " + str(POT))
                players.setStatus("Call")
                print("Player status is: " + str(players.checkStatus()))

            elif(inputPlayerConfirm == "N"):
                print("Understood! Returning to main menu.")
            else:
                print("You did not enter the right input to confirm or deny the call")
                bettingPhase(players)
        else:
            print("You entered the wrong input, returning to main menu.")
            bettingPhase(players)


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

    bettingPhase(players[0])

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
