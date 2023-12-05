from __future__ import annotations
from typing import List
from simple_types import Tile, RED, BLUE, YELLOW, GREEN, BLACK, compress_tile_list
from tileSources import TileSource
from bag import Bag
from tileSources import tableCenter

class Factory(TileSource):
    self.bag: Bag
    self.tableCenter: tableCenter
    def __init__(self, bag: Bag, tableCenter: tableCenter) -> None:
        self.bag = bag
        self.tableCenter = tableCenter
        super.__init__(self)
        pass
    
    def startNewRound(self) ->None:
        self.tiles = self.bag.take(4)

    def take(self, idx: int):
        taking: List[Tile] = super.take()
        self.tableCenter.add(self.tiles)
        self.tiles = []
        return taking
