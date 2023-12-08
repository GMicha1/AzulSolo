from __future__ import annotations
from typing import List
from simple_types import Tile, compress_tile_list, Points, RED, BLUE, YELLOW, GREEN, BLACK, STARTING_PLAYER
from board import Board
from usedTiles import usedTiles
from bag import Bag
from tableArea import TableArea
from customErrors import NotPlayersTurn, GameIsOver, EmptySourceOrWrongColour 
from interfaces import FinishRoundResult
from game_observer import GameObserver
#bruteforce is used on things I realized too late to discuss it with the team

class Game:
    _playerBoards: List[Board]
    _table: TableArea
    currentPlayer: int
    gameOver: bool
    nextFirst: int
    gameObserver: GameObserver
    bag: Bag
    def __init__(self, numOfPlayers: int, names: List[str] = list(), startPlayer: int = 0) -> None:
        self.gameOver = False
        self.nextFirst = startPlayer
        self._observer = GameObserver
        self.currentPlayer = self.nextFirst
        self._playerBoards = list()
        used_tiles: usedTiles = usedTiles()
        self.bag = Bag(used_tiles)
        self._table: TableArea = TableArea(numOfPlayers, self.bag)
        player_names: List[str] = names.copy()
        for i in range(numOfPlayers):
            if(player_names):
                self._playerBoards.append(Board(used_tiles, player_names.pop(0)))
            else:
                self._playerBoards.append(Board(used_tiles))

        self._table.startNewRound()
        #Strating player in center because __init__
        state: str = self.stateTable() + self.state()
        self._observer.notifyEverybody(state)
    
    def take(self, playerId:int, sourceId: int, idx:int, destinationIdx:int) -> None:
        if(self.gameOver):
            raise GameIsOver
        if(playerId != self.currentPlayer):
            raise NotPlayersTurn
        if(sourceId < -1):
            raise ValueError("Invalid source index")
        
        takenTiles: List[Tile] = self._table.take(sourceId, idx)
        if((not takenTiles)):
            raise EmptySourceOrWrongColour
        if(STARTING_PLAYER in takenTiles):
            self.nextFirst = self.currentPlayer #not using boards bool, it resets easily

        ####UNSURE IF WRONG INDEX IS OK, or it goes to floor and then still raises idx exception
        currentBoard = self._playerBoards[self.currentPlayer]
        currentBoard.put(destinationIdx, takenTiles)
        
        if(self._table.isRoundEnd()):
            self.finishRound()
            self.currentPlayer = self.nextFirst
        else:
            self.currentPlayer = (self.currentPlayer + 1)% len(self._playerBoards)

        state: str = ""
        if(not self.gameOver):
            state += self.stateTable()
        state += self.state()
            
        self._observer.notifyEverybody(state)

    def finishRound(self) -> None: #pomocna metoda
        for board in self._playerBoards:
            roundOver = board.finishRound()
            if(roundOver == FinishRoundResult.GAME_FINISHED):
                self.gameOver = True

        ##winners, points special state
        if(self.gameOver):
            winner: Board = self._playerBoards[0]
            for board in self._playerBoards:
                board.endGame()
                if(board._points.value > winner._points.value):
                    winner = board
            self.nextFirst = len(self._playerBoards)
            win: str = f"The winner is {winner._player_name} with {str(winner._points)} points!"
            self._observer.notifyEverybody(win)
            return
        self._observer.notifyEverybody("Starting new round... \n")

        self.startNewRound()
    def stateTable(self) -> str:
        state:str = self._table.state() + "\n"
        state +=  self.bag.state() + "\n"
        return state

    def state(self) -> str:
        state:str = ""
        for i in self._playerBoards:
            if(self.currentPlayer < len(self._playerBoards)
               and i == self._playerBoards[self.currentPlayer]):
                state += "\nThis player takes tiles next:"
            state += "\n" + i.state() + "\n"
            for j in i._pattern_line:
                state += j.stateWithWall() + "\n"
            state += i._floor.state() + "\n"
            
        return state

    def startNewRound(self) -> None: #pomocna metoda
        self._table.startNewRound()
        self._table.tableCenter.startNewRound() #bruteforce since tableCenter restart not in table
        


