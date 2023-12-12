from __future__ import annotations
from typing import List
from simple_types import Tile, compress_tile_list, RED
from usedTiles import usedTiles
from bag import Bag
import random
import unittest

class testBag(unittest.TestCase):
    def setUp(self) -> None:
        self.usedTiles = usedTiles()
        self.bag: Bag = Bag(self.usedTiles)

    def testingBag(self) -> None:
        self.assertEqual(self.bag.state(), 'In bag -> R:20 B:20 Y:20 G:20 L:20 ')
        tilesStr0: str = self.bag.stateList()
        takenTiles0: List[Tile] = self.bag.take(25, True, 0)
        #with seed 0 and 100 tiles in bag, ranrange int stays 49
        self.assertEqual(compress_tile_list(takenTiles0), tilesStr0[49: 49 + 25])
        self.assertEqual(self.bag.state(), 'In bag -> R:15 B:15 Y:15 G:15 L:15 ')
        takenTiles1: List[Tile] = self.bag.take(80)
        self.assertEqual(len(takenTiles1), 75)
        self.assertEqual(self.bag.state(), "The bag is empty")
        takenTiles2: List[Tile] = self.bag.take(4)
        self.assertEqual(takenTiles2, list())
        self.usedTiles.tiles = [RED, RED, RED, RED]
        takenTiles3: List[Tile] = self.bag.take(1)
        self.assertEqual(takenTiles3, [RED])
        self.assertEqual(self.bag.state(), 'In bag -> R:3 B:0 Y:0 G:0 L:0 ')


if __name__ == '__main__':
    unittest.main()
