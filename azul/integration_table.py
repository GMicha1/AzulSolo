from __future__ import annotations
import unittest
from typing import List
from simple_types import Tile, STARTING_PLAYER, RED, GREEN, Points
from bag import Bag
from tableArea import TableArea
from tileSources import tableCenter
from factory import Factory
from usedTiles import usedTiles

class testTable(unittest.TestCase):
    def setUp(self) -> None:
        self.usedTiles: usedTiles = usedTiles()
        self.bag: Bag = Bag(self.usedTiles)
        self.table: TableArea = TableArea(2, self.bag)
        self.center: tableCenter = self.table.tableCenter

    def test_TableArea(self) -> None:
        self.assertEqual(self.table.state(), "Factories: /\\ /\\ /\\ /\\ /\\ | Center: S")
        self.table.take(-1, 0)
        self.assertTrue(self.table.isRoundEnd())
        self.table.startNewRound()
        self.center.startNewRound()
        self.assertEqual(len(self.bag.stateList()), 80)

        with self.assertRaises(ValueError):
            self.table.take(5 , 2)
            
        self.table.factories[1].tiles = [RED, GREEN, GREEN, RED]
        takenTiles0: List[Tile] = self.table.take(1, 1)
        self.assertEqual(self.table.factories[1].state(), "/\\")
        self.assertEqual(self.center.state(), "SGG")
        self.assertFalse(self.table.isRoundEnd())

        self.table.factories[2].tiles = [RED, RED, RED, GREEN]
        takenTiles1: List[Tile] = self.table.take(2, 2)
        self.assertEqual(takenTiles1, list())
        self.assertEqual(self.table.factories[2].state(), "/RRRG\\")

        takenTiles2: List[Tile] = self.table.take(-1, 4)
        self.assertTrue(self.center.isEmpty())


        for i in range(4):
            self.table.startNewRound()   
        self.assertEqual(self.bag.state(), "The bag is empty")
        self.usedTiles.give([STARTING_PLAYER] + [RED] * 10 + [GREEN] * 4)
        self.assertEqual(self.usedTiles.state(), "R" * 10 + "G" * 4)

        self.table.startNewRound()
        self.assertEqual(self.usedTiles.state(), "")
        self.assertEqual(len(self.table.factories[3].state()), 4) #2 tiles and /\\
        self.assertTrue(self.table.factories[4].isEmpty())

        self.table.startNewRound() #starting round with empty bag And empty used tiles
        self.assertTrue(self.table.isRoundEnd())
        
        
if __name__ == '__main__':
    unittest.main()
