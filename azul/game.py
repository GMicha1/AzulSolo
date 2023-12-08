from __future__ import annotations
from typing import List
from simple_types import Tile, compress_tile_list, Points, RED, BLUE, YELLOW, GREEN, BLACK, STARTING_PLAYER
from board import Board
from usedTiles import usedTiles
from bag import Bag
from tableArea import TableArea
import customErrors 

class Game:
    _playerBoards: List[Board]
    _table: TableArea
    currentPlayer: int
    gameOver: bool
    def __init__(self, numOfPlayers: int, names: List[str] = list(), startPlayer: int = 0) -> None:
        gameOver = False
        self.currentPlayer = startPlayer
        self._playerBoards = list()
        used_tiles: usedTiles = usedTiles()
        self._table: TableArea = TableArea(numOfPlayers, Bag(used_tiles))
        player_names: List[str] = names.copy()
        for i in range(numOfPlayers):
            if(player_names):
                self._playerBoards.append(Board(used_tiles, player_names.pop(0)))
            else:
                self._playerBoards.append(Board(used_tiles))

        self._table.startNewRound()
        #Strating player in center because __init__
    
    def take(self, playerId:int, sourceId: int, idx:int, destinationIdx:int) -> None:
        if(gameOver):
            raise GameIsOver
        if(playerId != currentPlayer):
            raise NotPlayersTurn
        if(sourceId < -1):
            raise ValueError("Invalid source index")
        
        takenTiles = self._table.take(sourceId, idx)
        if((not takenTiles) or takenTiles == [STARTING_PLAYER]):
            raise EmptySourceOrWrongColour
        self._playerBoards[currentPlayer].put(destinationIdx:int, takenTiles)
        
        if(self._table.isRoundEnd):
            ###finishRound
            #startNewRound

    def startNewRound(self):
        pass
        


