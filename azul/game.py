from __future__ import annotations
from typing import List
from simple_types import Tile, compress_tile_list, Points, RED, BLUE, YELLOW, GREEN, BLACK
from board import Board
from usedTiles import usedTiles
from bag import Bag
from tableArea import TableArea
class Game:
    _playerBoards: List[Board]
    _table: TableArea
    currentPlayer: int
    def __init__(self, numOfPlayers: int, names: List[str] = list(), startingPlayer: int = 0) -> None:
        if(numOfPlayers < 2 or numOfPlayers > 4):
            raise ValueError("Invalid number Of Players")
        self.currentPlayer = startingPlayer
        self._playerBoards = list()
        used_tiles: usedTiles = usedTiles()
        self._table: TableArea = TableArea(numOfPlayers, Bag(used_tiles))
        player_names: List[str] = names.copy()
        while(len(player_names) <= numOfPlayers):
            player_names.append("")
            
        for name in player_names[:numOfPlayers]:
            self._playerBoards.append(Board(used_tiles, name))

        self._table.startNewRound()
        #Strating player in center because __init__
    
    def take(self) -> None:
        pass

    def startNewRound(self):
        pass
