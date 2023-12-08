from __future__ import annotations
from typing import List, Optional
from simple_types import Tile, Points, RED, BLUE, YELLOW, GREEN, BLACK, STARTING_PLAYER, compress_tile_list
from wallLine import WallLine
from floor import Floor
from usedTiles import usedTiles

#P = patternLine(3, Floor([Points(1), Points(2)], usedTiles()),
#usedTiles(), WallLine([RED, BLACK, GREEN, BLUE, YELLOW]))
class patternLine:
    capacity: int 
    _tilesInLine: List[Tile]
    _wallLine: WallLine
    _floor: Floor
    used_tiles: usedTiles
    def __init__(self, capacity: int, floor: Floor,
                 usedTiles: usedTiles, wallLine: WallLine) -> None:
        self.capacity = capacity
        self._tilesInLine = list()
        self._floor = floor
        self._wallLine = wallLine
        self.used_tiles = usedTiles
    
    def put(self, tiles: List[Tile]) -> None:
        if(tiles == list()):
            return
        if(tiles[0] in self._tilesInLine or (not self._tilesInLine)):
            self._tilesInLine.extend(tiles)
            tiles = list()
            if(len(self._tilesInLine) > self.capacity):
                tiles = self._tilesInLine[self.capacity:]
                self._tilesInLine = self._tilesInLine[:self.capacity]
        self._floor.put(tiles)
    
    def finishRound(self) -> Points:
        if(self._tilesInLine and len(self._tilesInLine) == self.capacity):
            if(not self._wallLine.canPutTile(self._tilesInLine[0])):
                self._floor.put(self._tilesInLine)
                self._tilesInLine = list()
                return Points(0)
            points: Points = self._wallLine.putTile(self._tilesInLine.pop())
            self.used_tiles.give(self._tilesInLine)
            self._tilesInLine = list()
            return points
        return Points(0)
    
    def state(self) -> str:
        state: str = compress_tile_list(self._tilesInLine)
        state += (self.capacity - len(state)) * "-"
        return state

    def stateWithWall(self) -> str:
        stateWithWall:str = self._wallLine.state()
        return stateWithWall + "| <- |" + self.state()
