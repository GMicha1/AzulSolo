from __future__ import annotations
from typing import List
import random
from game import Game
from customErrors import NotPlayersTurn, GameIsOver, EmptySourceOrWrongColour, NonViableColorIdx, WrongStartInfo

class GameInterface:
    numOfPlayers: int = 0
    names: List[str] = list()
    your_game: Game
    def __init__(self) -> None:
        self.numOfPlayers = 0
        self.names = list()
        #self.startNewGame() normally initiated so no need to test empty your_game

    def GUIpt1(self) -> None:
        if(self.numOfPlayers and self.names):
            reuse: str = input("Do you wish to use previous player data? Y/N")
            if(reuse == "Y" or reuse == "y"):
                return
            elif(reuse != "N" or reuse != "n"):
                print("Unrecognized input, evaluated as N")
            print("Please enter new data:")

        self.numOfPlayers = int(input("Enter number of players between 2 to 4"))
        while(self.numOfPlayers < 2 or self.numOfPlayers > 4):
            print("Invalid number of players.")
            self.numOfPlayers = int(input("Enter number of players between 2 to 4"))
        self.names = list()
        name: str = ""
        for i in range(self.numOfPlayers):
            name = input(f"May player{i} please enter their name")
            if(not name):
                print("proceeding with the rest of the players unnamed")
                break
            if(i > 0 and name in self.names):
                counter = 2
                while(name + str(counter) in self.names):
                    counter += 1
                name += str(counter)
                print(f"Your name was changed to {name}, for the original one is taken")
            self.names.append(name)


    def GUIpt2(self) -> int:
        startPId: int = 0
        startP:str = input("Which player wants to go first?")
        if(startP in self.names):
            startPId = self.names.index(startP)
        elif(startP in [str(i) for i in range(0, self.numOfPlayers)]):
            startPId = int(startP)
        else:
            print("There is no player like that, choosing starting player at random.")
            startPId = random.randrange(0, self.numOfPlayers)
        return startPid
        "Game START"

    def inputTake(self, pId) -> str: #unused function present just because
        playerId: int = pId # IRL would be implicit from input sender hopefully?
        sourceId: int = int(input("From which source? (center: -1)"))
        idx: int = int(input("Which color? S: 0, R: 1, B: 2, Y: 3, G: 4, L: 5"))
        destinationIdx: int = int(input("Where should it go?"))
        self.take(playerId, sourceId, idx, destinationIdx)
        
    def startNewGame(self, testNumOfPlayers:int = 0,
                     testNames: List[str] = list(), testFirst: int = 0) -> None:
        startPId: int = 0
        if(testNumOfPlayers):
            if(testNumOfPlayers > 4 or testNumOfPlayers < 2):
                raise WrongStartInfo
            self.numOfPlayers = testNumOfPlayers
            self.names = testNames
            if(testFirst < testNumOfPlayers and testFirst >= 0):
                startPId = testFirst
        else:
            self.GUIpt1()
            startPId = self.GUIpt2()
            
        self.your_game = Game(self.numOfPlayers, self.names, startPId)
        
    def take(self, playerId:int, sourceId: int, idx:int, destinationIdx:int) -> bool:
        try:
            self.your_game.take(playerId, sourceId, idx, destinationIdx)
            return True
        except ValueError:
            print("Incorrect source index.")
            return False
        except NotPlayersTurn:
            print("Right now is a different players turn.")
            return False
        except GameIsOver:
            print("This game is already over.")
            return False
        except EmptySourceOrWrongColour:
            print("Your specified source either does not have this color or is empty.")
            return False
        except NonViableColorIdx:
            print("You have chosen a non-viable color option.")
