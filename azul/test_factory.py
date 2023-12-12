from __future__ import annotations
from typing import List
from simple_types import Tile, BLUE, BLACK
from bag import Bag
from usedTiles import usedTiles
from tileSources import tableCenter
from factory import Factory
import unittest


class TestFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.factory: Factory = Factory(Bag(usedTiles()), tableCenter())
        self.factoryBag: Bag = self.factory.bag

    def test_factory(self) -> None:
        self.assertTrue(self.factory.isEmpty())
        takenTiles0: List[Tile] = self.factory.take(1)
        self.assertEqual(takenTiles0, list())
        self.factoryBag.tiles = [BLUE] * 4
        self.factory.startNewRound()
        self.assertEqual(self.factory.state(), "/BBBB\\")
        self.assertFalse(self.factory.isEmpty())
        self.factoryBag.tiles = [BLUE] * 2 + [BLACK] * 2
        self.factory.startNewRound()
        takenTiles1: List[Tile] = self.factory.take(1)#indexes should be fine, tested elsewhere
        self.assertEqual(takenTiles1, list())
        self.assertEqual(len(self.factory.tiles), 4)
        takenTiles2: List[Tile] = self.factory.take(2)
        self.assertEqual(takenTiles2, [BLUE]*2)
        self.assertEqual(self.factory.state(), "/\\")
        #dont know if I should test if the rest is in table center, sound like integration test
if __name__ == '__main__':
    unittest.main()
