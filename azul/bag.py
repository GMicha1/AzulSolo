from __future__ import annotations
from typing import List
from simple_types import Tile, RED, BLUE, YELLOW, GREEN, BLACK, compress_tile_list
from usedTiles import usedTiles

class Bag:
    self.used_tiles: usedTiles
    def __init__(self, used_tiles: usedTiles) -> None:
        self.used_tiles = used_tiles
        pass

    def state(self) -> str:
        pass

    def take(self, count: int) -> list[Tile]:
        pass
