from __future__ import annotations
from typing import List
import unittest
from simple_types import Tile, compress_tile_list, Points, RED, BLUE, YELLOW, GREEN, BLACK, STARTING_PLAYER
from board import Board
from usedTiles import usedTiles
from bag import Bag
from floor import Floor
from tableArea import TableArea
from customErrors import NotPlayersTurn, GameIsOver, EmptySourceOrWrongColour, NonViableColorIdx, WrongStartInfo
from interfaces import FinishRoundResult
from game_observer import GameObserver
from gameInterface import GameInterface
from game import Game

class TestFullGame(unittest.TestCase):
    g_I: GameInterface
    game: Game
    used_tiles: usedTiles
    bag: Bag
    table: TableArea
    boards: List[Board]
    def setUp(self) -> None:
        self.g_I = GameInterface()
    def test_full_game(self) -> None:
        with self.assertRaises(WrongStartInfo):
            self.g_I.startNewGame(5, ["A", "B"], 4)
            
        self.g_I.startNewGame(3, ["A", "B"], 10) #starting player defults to 0 if invalid id
        self.assertEqual(self.g_I.your_game.currentPlayer, 0)
        numOfFactories: int = len(self.g_I.your_game._table.factories)
        self.assertEqual(numOfFactories, 7)

        self.g_I.startNewGame(2, ["A"], 1)
        self.game = self.g_I.your_game
        self.bag = self.game.bag
        self.used_tiles = self.bag.used_tiles
        self.assertEqual(self.used_tiles.state(), "")
        self.table = self.game._table
        self.boards = self.game._playerBoards
        bagSizeAtStart: int = len(self.bag.stateList())
        self.assertEqual(bagSizeAtStart, 100 - 5*4)
        with self.assertRaises(NotPlayersTurn):
            self.game.take(0, 2, 3, 4)
        self.assertFalse(self.g_I.take(1, 5, 3, 4))#factories are 0-4
        #raised exception returned false, so others will too

        self.table.factories[0].tiles = [RED, RED, BLUE, YELLOW]
        self.assertTrue(self.g_I.take(1, 0, 3, 4))
        self.assertEqual(self.boards[1]._pattern_line[4].state(),"Y----")

        self.assertFalse(self.g_I.take(0, 0, 1, 1))#empty factory from last turn
        self.assertTrue(self.g_I.take(0, -1, 2, 0))
        self.assertEqual(self.boards[0]._floor.state(), "S")
        self.assertEqual(self.table.tableCenter.state(), "RR")
        self.assertEqual(self.game.nextFirst, 0)

        self.assertFalse(self.table.factories[1].isEmpty())
        self.table.factories[1].tiles = [RED, RED, BLUE, BLUE]
        self.assertFalse(self.g_I.take(1, 1, 3, 1))#wrongColor
        self.g_I.take(1, 1, 2, 0)
        for i in self.table.factories:
            i.tiles = list()
        self.g_I.take(0, -1, 1, 3)

        predictedState0: str = """
This player takes tiles next:
A: has number of points 1
-B---| <- |-
-----| <- |--
-----| <- |---
---R-| <- |----
-----| <- |-----


: has number of points 0
-B---| <- |-
-----| <- |--
-----| <- |---
-----| <- |----
-----| <- |Y----

"""
        self.assertEqual(self.game.state(), predictedState0)
        self.assertEqual(bagSizeAtStart - 5*4, len(self.bag.stateList()))
        self.assertEqual(self.used_tiles.state(), "RRRB")
        
        ###########everything seemingly works so testing end of game
        self.boards[0]._wall[0].putTile(YELLOW)
        self.boards[0]._wall[0].putTile(GREEN)
        self.boards[0]._wall[0].putTile(BLACK)
        self.boards[0]._wall[1].putTile(BLUE)
        self.boards[0]._wall[2].putTile(RED)
        self.boards[0]._wall[2].putTile(YELLOW)
        self.boards[0]._wall[3].putTile(GREEN)
        self.boards[0]._wall[4].putTile(BLUE)
        self.boards[0]._wall[4].putTile(GREEN)

        self.boards[1]._wall[0].putTile(YELLOW)
        self.boards[1]._wall[1].putTile(BLUE)
        self.boards[1]._wall[1].putTile(RED)
        self.boards[1]._wall[2].putTile(BLUE)
        self.boards[1]._wall[2].putTile(BLACK)
        self.boards[1]._wall[3].putTile(GREEN)
        self.boards[1]._wall[3].putTile(BLACK)
        self.boards[1]._wall[3].putTile(BLUE)
        self.boards[1]._wall[4].putTile(BLUE)
        self.boards[1]._wall[4].putTile(YELLOW)
        self.boards[1]._wall[4].putTile(GREEN)

        self.bag.tiles = [RED, RED]
        self.game.startNewRound()
        self.assertEqual(len(self.table.factories[2].state()), 2 + 0)
        self.assertEqual(len(self.table.factories[1].state()), 2 + 2)
        self.table.factories[0].tiles = [RED, RED, RED, RED]
        self.table.factories[1].tiles = [RED, BLUE]


        self.g_I.take(0, 1, 1, 0)
        self.g_I.take(1, 0, 1, 2)
        self.assertTrue(self.g_I.take(0, -1, 2, 0))
        
        self.assertFalse(self.g_I.take(0, -1, 0, 0))
        basePointsA: int = 1 + 5 - 2 #before, placement points, floor
        finalPointsA: int = 2
        basePointsB: int = 0 + 8 - 1
        finalPointsB: int = 7 + 7 + 10
        predictedState1: str = f"""
A: has number of points {basePointsA + finalPointsA}
RBYGL| <- |-
--B--| <- |--
--R-Y| <- |---
-G-R-| <- |----
B-G--| <- |-----


: has number of points {basePointsB + finalPointsB}
-BY--| <- |-
-RB--| <- |--
-LRB-| <- |---
-GL-B| <- |----
BYG--| <- |Y----

"""
        self.assertEqual(self.game.state(), predictedState1)
if __name__ == '__main__':
    unittest.main()
