from __future__ import annotations
from typing import List, Optional
from azul.simple_types import Tile, Points, RED, BLUE, YELLOW, GREEN, BLACK, STARTING_PLAYER
from wallLine import WallLine
from floor import Floor

class WallLine:
    capacity: int 
    _tilesInLine: List[Optional[Tile]]
    _wallLine: WallLine
    _floor: Floor
    def __init__(self, capacity: int, floor: Floor, usedTiles: usedTiles, wallLine: WallLine) -> None:
        self.capacity = capacity
        self.tilesInList = list()
        self._floor = floor
        self.wallLine = wallLine
    
    def put(self, tiles[Tile]) -> None:
        pass
    
    def finishRound(self) -> Points:
        pass
    
    def state(self) -> str:
        pass
