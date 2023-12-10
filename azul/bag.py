from __future__ import annotations
from typing import List
from simple_types import Tile, RED, BLUE, YELLOW, GREEN, BLACK, compress_tile_list
from usedTiles import usedTiles
import random

class Bag:
    used_tiles: usedTiles
    tiles: List[Tile]
    def __init__(self, used_tiles: usedTiles) -> None:
        self.used_tiles = used_tiles
        self.tiles = [RED, BLUE, YELLOW, GREEN, BLACK]*20
        pass

    def state(self) -> str:
        if (not self.tiles):
            return "The bag is empty"
        state: str = "In bag -> "
        for tileType in [RED, BLUE, YELLOW, GREEN, BLACK]:
            state += str(tileType) + ":" + str(self.tiles.count(tileType)) + " "
        return state

    def stateList(self) -> str:
        if(not self.tiles):
            return ""
        return compress_tile_list(self.tiles)

    def take(self, count: int, testing: bool = False) -> List[Tile]:
        taken: List[Tile] = list()
        for i in range(count):
            if(not self.tiles):
                self.tiles = self.used_tiles.takeAll()
                if(not self.tiles):
                    #"Insuficient number of tiles"
                    break
            if(testing):#pseudorandomForTesting (hopefully)
                idxOfTile = 0
            else:
                idxOfTile = random.randrange(0,len(self.tiles))
            taken.append(self.tiles.pop(idxOfTile))
        return taken
