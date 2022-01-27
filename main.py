# Dev - Amp
# Project - Nim Type Zero
# Last Modified 1/27/2022

# TODO
# Add getter methods as more properties in the player object are made
# Implement betting logic
# seperate actions into bot methods and human methods
# folding after open also crashes game - bots seemingly cannot continue to function without player playing
# Also need to subtract difference between highest bet and current bet not highest bet + current bet
# Ability to fold after opening is broken. Need to remind game that player has folded.
# No current end state for betting phase (all bots calling once and then player calling) for betting phase.
# Float input for betting amounts crashes game.
# Need a way to push to "reward" for playing phase.

# GLOBAL ASS VARIABLES - SIN DO NOT COMMIT THIS HERESY LATER

CARDTAGS = ["Spades", "Hearts", "Diamonds", "Clubs"]

VERSION = "3.0"

POT = 0
TURN_COUNT = 0
ROUND_COUNT = 0


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
        return os_linesep + "This is " + self.name + "'s Hand:" + os_linesep + os_linesep.join([str(x) for x in self.hand]) + os_linesep + self.name + 's money: ' + str(self.money)

    def draw(self, deck, numCards):  # method that allows one player to draw all four cards for their hand at once
        for _ in range(numCards):
            self.hand.append(deck.drawOneCard())

    # Debug tool that may actually get used later to pull player names in game
    def whatIsName(self):
        return self.name

    def checkMoney(self):
        return self.money

    def subMoney(self, betAmount):
        self.money = self.money - betAmount

    def transferMoney(self, amount):
        self.subMoney(amount)
        addPot(amount)

    def fold(self):
        self.status = "Fold"
        print(self.whatIsName() + " has folded")

    def open(self):
        self.status = "Open"
        if self.isHuman:
            return self.player_open()
        else:
            return self.bot_open()

    def bet(self, highest_bet):
        self.status = "Bet"
        if self.isHuman:
           return self.player_bet(highest_bet)
        else:
           return self.bot_bet(highest_bet)

    def setStatus(self, status):
        self.status = status

    def checkStatus(self):
        return self.status


    ## implement human logic methods
    def player_open(self):
        # TODO: add something to catch float input
        print(self.whatIsName() + " has been chosen to Open or Fold")
        print("{0}Betting Options: {0} 1.) Open {0} 2.) Fold".format(os_linesep))
        openChoice = int(input("Which do you choose?{}".format(os_linesep)))

        if (openChoice == 1):
            print("You have chosen to open. How much are you opening with?")
            openingAmount = int(input("Enter an amount to open with: ".format(os_linesep)))
            if (openingAmount <= 0):
                print("You cannot open with nothing.")
                return -1
            elif (openingAmount > self.checkMoney()):
                print("To open the amount of: {} you need more money. Try betting lower{}".format(openingAmount, os_linesep))
                return -1
            else:
                print("You have chosen to Open with: {0}{1}".format(openingAmount, os_linesep))
                self.transferMoney(openingAmount)
                print("Current Pot: " + str(POT) + " Money left: " + str(self.checkMoney()) + " Opening Bet: " + str(openingAmount) + " {}".format(os_linesep))

        elif (openChoice == 2):
            print("You have chosen to fold. You will not be participating this round.")
            self.fold()
        else:
            print("Not a Valid Input. Try again.")
            return -1
        return openingAmount

    def player_bet(self, highest_bet):
        global TURN_COUNT
        # TODO: add something to catch float input
        print("Current highest bet is ", highest_bet)
        print("{0}Betting Options: {0} 1.) Fold {0} 2.) Raise {0} 3.) Call".format(os_linesep))
        playerChoice = input("Which do you choose? {}".format(os_linesep))
        bettingAmount = 0
        if (playerChoice == "1"):
            print("You chosen to fold, you will not play this round{}".format(os_linesep))
            self.fold()
            return highest_bet
        elif (playerChoice == "2"):
            print("You have chosen to Raise, what are you betting?")
            bettingAmount = int(input("Enter an amount higher than the current pot: {0}{1}".format(highest_bet, os_linesep)))
            if (bettingAmount < highest_bet):
                print("To Raise you must bet more than current highest bet: {0}{1}".format(highest_bet, os_linesep))
                return -1
            elif (bettingAmount > self.checkMoney()):
                print("To Raise the amount of: '{}' You need more than {} money{}".format(highest_bet, self.checkMoney(), os_linesep))
                return -1
            else:
                print("You have chosen to Raise: {}{}".format(bettingAmount, os_linesep))
                self.transferMoney(bettingAmount)
                print("Current Money is: {} Current Highest Bet is: {}{}".format(self.checkMoney(), highest_bet, os_linesep))
                #TODO: change the rest of the formatting things
        elif (playerChoice == "3"):
            print("You have chosen to Call, you are matching the current open of: {}{}".format(highest_bet, os_linesep))
            inputPlayerConfirm = input("To confirm your call, type yes or no (Y/N)".format(os_linesep))
            if (inputPlayerConfirm == "Y"):
                if(self.checkMoney() >= highest_bet):
                    self.transferMoney(highest_bet)
                    bettingAmount = highest_bet
                    print("Current Money: " + str(self.checkMoney()))
                    print("Current Pot: " + str(POT))
                    self.setStatus("Call")
                    print("Player status is: " + str(self.checkStatus()))
                else:
                    print("Your amount of money does not match current highest bet")
                    return -1
                TURN_COUNT += 1

            elif (inputPlayerConfirm == "N"):
                print("Understood! Returning to main menu.")
                return -1
            else:
                print("You did not enter the right input to confirm or deny the call")
                return -1

        else:
            print("You entered the wrong input, returning to main menu.")
            return -1
        return bettingAmount

    def player_raise(self):
        ##do stuff
        pass

    def player_call(self):
        ##do stuff
        pass


    ## implement bot logic methods
    def bot_open(self):
        openChoice = random.choice([1,2])
        if openChoice == 1:
            openingAmount = random.randint(1, self.checkMoney())
            self.transferMoney(openingAmount)
        elif openChoice == 2:
            self.fold()
        return openingAmount

    def bot_raise(self):
        ##do bot stuff
        pass

    def bot_call(self):
        ##do bot stuff
        print("This bot has called")
        pass

    def bot_bet(self, highest_bet):
        global TURN_COUNT
        playerChoice = random.choice(["1", "2", "3"])
        if self.checkMoney() < highest_bet:
            playerChoice = "1"
        bettingAmount = 0
        if (playerChoice == "1"): # Fold
            self.fold()
            return highest_bet
        elif (playerChoice == "2"): # Raise
            bettingAmount = random.randint(highest_bet, self.checkMoney())
            if (bettingAmount < highest_bet):
                return -1
            if (bettingAmount > self.checkMoney()):
                bettingAmount = self.checkMoney()
                print(self.whatIsName(), " has chosen to Raise ", bettingAmount, " money")
                print(self.whatIsName() +" status is: " + str(self.checkStatus()))
                self.transferMoney(bettingAmount)
                return bettingAmount
            else:
                self.transferMoney(bettingAmount)
                print(self.whatIsName(), " has chosen to Raise ", bettingAmount, " money")

                # TODO: change the rest of the formatting things
        elif (playerChoice == "3"): # Call
            if (self.checkMoney() >= highest_bet):
                print(self.whatIsName(), " has chosen to Match/Call ", highest_bet, " money")
                self.transferMoney(highest_bet)
                print("Current Money for " + self.whatIsName() + " " + str(self.checkMoney()))
                bettingAmount = highest_bet
                self.setStatus("Call")

                TURN_COUNT += 1
            else:
                return -1
        print("Current Pot: " + str(POT))
        return bettingAmount


# FUNCTIONS
def isOpen():
    if(POT == 0):
        return True

def addPot(betAmount):
    global POT
    POT += betAmount


def bettingPhase(players):
    global TURN_COUNT
    global POT
    ## This logic determines if a player is the first to open or not
    ## TODO: Add while loop
    highest_bet = 0
    while(True):

        for player in players:
            if(isOpen()): #checks to see if player is opening the bet
                result = -1
                while (result == -1):
                    result = player.open()
                highest_bet = result
            else:
                result=-1
                while(result==-1):
                    result = player.bet(highest_bet)
                highest_bet = result






    # Implement betting Logic later

def initiate(players):
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

    # draw players hands
    for player in players:
        player.draw(testDeck, 4)

    # print players hands
    # for player in players:
    #    print(player)

    print('Hello! Welcome to Nim Type Zero ' + players[0].whatIsName())

    # Reminder for later: os_linesep logic adds the VERSION global
    # variable to sub for the first {}, and then a newline for the second {}
    print('Ver: {}{}'.format(VERSION, os_linesep))

    print(players[0])

    #adds all players into betting phase
    bettingPhase(players)

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
playerList[0].isHuman = True

initiate(playerList)
