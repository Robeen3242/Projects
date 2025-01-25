"""
Title: Game Class
Author: Robin Liu
Date: 2023-03-24
"""

from dice import Dice
from player import Player

class Game:
    def __init__(self):
        self.TURN = 0
        self.PLAYERS = []
        self.TOP_SCORE = [0, "No one"]
        self.TEAMS = False
            


    def run(self):
        while True:
            #INPUTS
            self.title()
            self.createPlayers()
            #PROCESSING
            if self.TEAMS == False:
                #PROCESSING
                for i in range(len(self.PLAYERS)):
                    self.PLAYERS[i] = Player(self.PLAYERS[i])
                    self.playerTurn(self.PLAYERS[i])
                    #OUTPUTS
                    self.getHighestScore(self.PLAYERS[i])
                print(f"{self.TOP_SCORE[1]} won the game!")
            else:
                #PROCESSING
                for i in range(len(self.PLAYERS)):
                    self.PLAYERS[i] = Player(self.PLAYERS[i])
                    self.playerTurn(self.PLAYERS[i])
                #OUTPUTSself
                self.getTeamScore()
            self.again()
    
    def title(self):
        print('''Arrrr Matey, here be the world of pirates. You and yer crew haf'te sniff out the treasures 
        of the world. But wait! Other captains ARRRRRRRRRRRRRRRRR also trying ta' steal ye booty. Assemble
        yer crew! Times tickin', I reckon ye only have three days ter get yerself a schooner and a crew so 
        quick lad! Move yer [redacted], we got some booty to sniff. 
        
        Welcome to Booty Sniffer! A dice game to play with friends (if you have them). Each player will have
        to roll for a ship (6), before their captain (5), which is before their crew (4). You MUST roll all of these in order or together
        to be able to find gold in the remaining dice. It turns out that you may be able to assign the help
        of a professional on your crew. If two players have the same amount of gold, chances are they looted the same island and 
        so it is the early bird gets the worm type of deal.
        ''')
    
        
    def again(self):
        CHOICE = input("Would you to play again? (y/N)> ")
        if CHOICE.upper() == "YES" or CHOICE.upper() == "Y":
            pass
        elif CHOICE.upper() == "" or CHOICE.upper() == "N" or CHOICE.upper() == "NO":
            exit()
        else:
            print("Please put in a valid response.")
            return self.again()
    def playerTurn(self, PLAYER, HAND = []):
        print(f"IT'S {PLAYER.PLAYER.upper()}'s TURN {self.TURN + 1}")
        if self.TURN == 0:
            HAND = sorted(PLAYER.createHand())
            self.checkHand(PLAYER, HAND)
            print(HAND)
            if len(HAND) == 2:
                self.stayIn(PLAYER, HAND)
            else:
                self.TURN += 1
                return self.playerTurn(PLAYER, HAND)
        elif self.TURN == 1:
            HAND = self.rollHand(HAND)
            self.checkHand(PLAYER, HAND)
            print(HAND)
            if len(HAND) == 2:
                self.stayIn(PLAYER, HAND)
            else:
                self.TURN += 1
                return self.playerTurn(PLAYER, HAND)
        else:
            self.TURN = 0
            HAND = self.rollHand(HAND)
            self.checkHand(PLAYER,HAND)
            print(HAND)
            if PLAYER.CREW == False:
                print("You have not found the requirements to be a true pirate, therefore you got no gold!")
            elif len(HAND) == 2:
                print(f"This is your last turn. Your final gold is: {HAND[0] + HAND[1]}")

    def rollHand(self, HAND):
        DIE = Dice()
        for i in range(len(HAND)):
            DIE.rollDice()
            HAND[i] = DIE.NUMBER
        return HAND

    #mutator methods
    def getTeams(self):
        CHOICE = input("Would you like teams? (y/N)> ")
        if CHOICE.upper() == "YES" or CHOICE.upper() == "Y":
            self.TEAMS = True
        elif CHOICE.upper() == "" or CHOICE.upper() == "N" or CHOICE.upper() == "NO":
            pass
        else:
            print("Please put in a valid response.")
            return self.getTeams()
    def createPlayers(self):
        try:
            PLAYER_NUM = int(input("How many players are there? (Maximum: 4) > "))
        except ValueError:
            print("You did not put in a valid response. Please try again.")
            return self.createPlayers()
        if PLAYER_NUM < 2: 
            print("Get some friends you social reject.")
            return self.createPlayers()
        elif PLAYER_NUM > 4:
            print("Too much competition!")
            return self.createPlayers()

        if PLAYER_NUM == 4:
            self.getTeams()
            if self.TEAMS == True:
                print("""Team 1: Player 1 and Player 2
                Team 2: Player 3 and Player 4
                """)
        for i in range(PLAYER_NUM):
            self.PLAYERS.append((input(f"Player {i+1}: ")))

    #accessor methods

    def getHighestScore(self, PLAYER):
        if self.TEAMS == False:
            if PLAYER.SCORE > self.TOP_SCORE[0]:
                self.TOP_SCORE = [PLAYER.SCORE, PLAYER.PLAYER]

    def getTeamScore(self):
        TEAM_1 = self.PLAYERS[0].SCORE + self.PLAYERS[1].SCORE
        TEAM_2 = self.PLAYERS[2].SCORE + self.PLAYERS[3].SCORE
        if TEAM_1 > TEAM_2:
            print(f"{self.PLAYERS[0].PLAYER} and {self.PLAYERS[1].PLAYER} (TEAM 1) has won!")
        elif TEAM_1 == TEAM_2:
            print(f"Both teams have the same amount of gold! It's a tie!")
        else:
            print(f"{self.PLAYERS[2].PLAYER} and {self.PLAYERS[3].PLAYER} (TEAM 2) has won!")
            
    def stayIn(self, PLAYER, HAND):
        print(f"You have {HAND[0] + HAND[1]} gold.")
        CHOICE = input("Would you like to retire (Searching for more gold means you must ditch the gold you have now)? (y/N) ")
        if CHOICE.upper() == "YES" or CHOICE.upper() == "Y":
            PLAYER.SCORE = HAND[0] + HAND[1]
        elif CHOICE.upper() == "" or CHOICE.upper() == "N" or CHOICE.upper() == "NO":
            self.TURN += 1
            return self.playerTurn(PLAYER,HAND)
        else:
            print("Please put in a valid response.")
            return self.stayIn(PLAYER, HAND)

    def checkHand(self, PLAYER, HAND):
        for i in range(len(HAND)):
            if HAND[i-1] == 6 and PLAYER.SHIP == False:
                HAND.pop(i)
                PLAYER.setShip()
                print("SHIP FOUND!")
                return self.checkHand(PLAYER, HAND)
            if PLAYER.SHIP == True and HAND[i-1] == 5 and PLAYER.CAPTAIN == False:
                HAND.pop(i)
                PLAYER.setCaptain()
                print("CAPTAIN FOUND")
                return self.checkHand(PLAYER, HAND)
            if PLAYER.SHIP == True and PLAYER.CAPTAIN == True and HAND[i-1] == 4 and PLAYER.CREW == False:
                HAND.pop(i)
                PLAYER.setCrew()
                print("CREW FOUND!")
        




if __name__ == "__main__":
    GAME = Game()
    GAME.run()