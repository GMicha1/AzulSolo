from __future__ import annotations
from typing import List
from simple_types import Tile, RED, BLUE, YELLOW, GREEN, BLACK, compress_tile_list
from tileSources import TileSource
from bag import Bag
from tileSources import tableCenter

class Factory(TileSource):
    bag: Bag
    tableCenter: tableCenter
    def __init__(self, bag: Bag, tableCenter: tableCenter) -> None:
        super().__init__()
        self.bag = bag
        self.tableCenter = tableCenter
    
    def startNewRound(self) -> None:
        self.tiles = self.bag.take(4)

    def take(self, idx: int) -> List[Tile]:
        taking: List[Tile] = super().take(idx)
        self.tableCenter.add(self.tiles)
        self.tiles = []
        return taking

    def state(self) -> str:
        state: str = super().state()
        return "/" + state + "\\"
