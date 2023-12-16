from typing import List
from simple_types import Points, Tile, STARTING_PLAYER, RED, BLUE, YELLOW, GREEN, BLACK
from patternLine import patternLine
from floor import Floor
from interfaces import FinishRoundResult
from wallLine import WallLine
from gameFinished import GameFinished
from finalPointsCalculation import FinalPointsCalculation
from usedTiles import usedTiles
from board import Board
import unittest


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        class fakeUsedTiles(usedTiles):
            def __init__(self) -> None:
                pass
            def give(self, tiles: List[Tile]) -> None:
                pass
        self.board: Board = Board(fakeUsedTiles(), "name")
        self.floor: Floor = self.board._floor
    def test_board(self) -> None:
        self.board.put(1, [RED, RED, RED])
        self.assertEqual(self.board._pattern_line[1].state(), "RR")
        self.assertEqual(self.floor.state(), "R")
        self.board.put(2, [STARTING_PLAYER, BLUE])
        self.board.put(6, [BLUE])
        self.board.put(2, [RED])
        self.assertEqual(self.floor.state(), "RSBR")
        
        self.board.put(3, [])
        self.assertEqual(self.board.state(), f"name: has number of points {0 + 1 - 6}")
        self.assertEqual(self.board._wall[1].state(), "-R---")
        line2State: str = self.board._pattern_line[2].stateWithWall()
        self.assertEqual(line2State, "-----| <- |B--")
        self.assertEqual(self.floor.state(), "")

        self.board.put(0, [BLUE])
        self.board.put(1, [BLACK, BLACK])
        self.board.put(2, [BLUE])
        self.board.put(3, [])
        self.assertEqual(self.board.state(), f"name: has number of points {-5 + 2 + 2 - 0}")
        self.assertEqual(self.board._pattern_line[2].state(), "BB-")

        self.board.put(0, [RED])
        self.board.put(1, [BLUE, BLUE])
        self.board.put(2, [BLUE])
        self.board.put(3, [GREEN]*4)
        self.board.put(4, [YELLOW]*5)
        self.board.finishRound()
        self.assertEqual(self.board._points.value, -1 + 4 + 3 + 1 + 1 + 2 - 0)
        self.board.put(1, [STARTING_PLAYER, YELLOW, YELLOW])
        self.board.put(2, [BLACK]* 3)
        self.board.put(3, [BLUE]*4)
        self.board.put(4, [BLUE]*5)
        entireState: str = self.board.state()
        for line in self.board._pattern_line:
            entireState += "\n" + line.stateWithWall()
        entireState += "\n" + self.floor.state()
        self.assertEqual(entireState,  f"name: has number of points {10}"
                         + "\n" + "RB---| <- |-"
                         + "\n" + "LRB--| <- |YY"
                         + "\n" + "---B-| <- |LLL"
                         + "\n" + "-G---| <- |BBBB"
                         + "\n" + "-Y---| <- |BBBBB"
                         + "\n" + "S")
        #self.board.put(-2, []) this exception does not end the game however it is not used in final product
        self.board.put(2, []) #POINTS 10 + 6 + 5 + 1 + 2 -1 = 23

        self.board.put(1, [GREEN]*5)
        self.assertEqual(self.board.finishRound(), FinishRoundResult.GAME_FINISHED)
        basePointValue: int = 23 + 5 - 1 -1 -2
        finalCalculations: int = 2 + 7 + 10
        self.assertEqual(self.board._points.value, basePointValue + finalCalculations)

if __name__ == '__main__':
    unittest.main()
