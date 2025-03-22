# Dice Class
"""
Title: Dice Object for Game
Author: Robin Liu
Date: 2023--03-23
"""

import random

class Dice:

    def __init__(self):
        self.NUMBER = 0

    #Modifier method
    def rollDice(self):
        self.NUMBER = random.randint(1,6)
