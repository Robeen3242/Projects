# Player Class
"""
Title: Dice Object for Game
Author: Robin Liu
Date: 2023--03-23
"""
from dice import Dice
class Player:

    def __init__(self, NAME=""):
        self.PLAYER = NAME
        self.CAPTAIN = False
        self.CREW = False
        self.SHIP = False
        self.SCORE = 0

    def createHand(self):
        HAND = []
        for i in range(5):
            DICE = Dice()
            DICE.rollDice()
            HAND.append(DICE.NUMBER)
        return HAND
    #modifier methods
    def setShip(self):
        self.SHIP = True

    def setCaptain(self):
        self.CAPTAIN = True

    def setCrew(self):
        self.CREW = True
