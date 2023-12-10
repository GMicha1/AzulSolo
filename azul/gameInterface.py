from __future__ import annotations
from typing import List
import random
from game import Game
from customErrors import NotPlayersTurn, GameIsOver, EmptySourceOrWrongColour, NonViableColorIdx

class GameInterface:
    numOfPlayers: int = 0
    names: List[str] = list()
    your_game: Game
    def __init__(self) -> None:
        self.numOfPlayers = 0
        self.names = list()
        self.startNewGame()

    def startNewGame(self) -> None:
        if(self.numOfPlayers and self.names):
            reuse: str = input("Do you wish to use previous player data? Y/N")
            if(reuse == "Y" or reuse == "y"):
                self.startNewGamePt2()
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
        self.startNewGamePt2()


    def startNewGamePt2(self):
        startPId: int = 0
        startP:str = input("Which player wants to go first?")
        if(startP in self.names):
            startPId = self.names.index(startP)
        elif(startP in [str(i) for i in range(0, self.numOfPlayers)]):
            startPId = int(startP)
        else:
            print("There is no player like that, choosing starting player at random.")
            startPId = random.randrange(0, self.numOfPlayers)
        self.your_game = Game(self.numOfPlayers, self.names, startPId)
        "Game START"
        
    def inputTake(self, pId) -> str: #unused function present just because
        playerId: int = pId # IRL would be implicit from input sender hopefully?
        sourceId: int = int(input("From which source? (center: -1)"))
        idx: int = int(input("Which color? S: 0, R: 1, B: 2, Y: 3, G: 4, L: 5"))
        destinationIdx: int = int(input("Where should it go?"))
        self.take(playerId, sourceId, idx, destinationIdx)
        
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
