from __future__ import annotations
from patternLine import patternLine
from simple_types import Tile, Points, RED, BLUE, YELLOW, GREEN, BLACK
from wallLine import WallLine
from floor import Floor
from usedTiles import usedTiles
import unittest


class TestPatternLine(unittest.TestCase):
    def setUp(self) -> None:
        used_tiles: usedTiles = usedTiles()
        self.patternLine: patternLine = patternLine(3, Floor([Points(1), Points(2)], used_tiles),
                                       used_tiles, WallLine([RED, BLUE, YELLOW, GREEN, BLACK]))

    def test_pattern_line(self) -> None:
        self.assertEqual(self.patternLine.state(), "---")

        self.patternLine.put([RED])
        self.assertEqual(self.patternLine.stateWithWall(), "-----| <- |R--")

        self.patternLine.put([BLUE])
        self.assertEqual(self.patternLine.state(), "R--")

        self.patternLine.put([RED])
        endRound0: Points = self.patternLine.finishRound()
        self.assertEqual(endRound0.value, 0)
        self.assertEqual(self.patternLine.stateWithWall(), "-----| <- |RR-")
        
        self.patternLine.put([RED]*5)
        self.assertEqual(self.patternLine._tilesInLine, [RED]*3)
        endRound1: Points = self.patternLine.finishRound()
        self.assertEqual(self.patternLine.stateWithWall(), "R----| <- |---")
        self.assertEqual(endRound1.value, 1)

        self.patternLine.put([BLUE]*4)
        endRound2: Points = self.patternLine.finishRound()
        self.assertEqual(endRound2.value, 2)

        self.patternLine.put([RED]*3)
        self.assertEqual(self.patternLine.state(), "RRR")
        endRound3: Points = self.patternLine.finishRound()
        self.assertEqual(endRound3.value, 0)
        self.assertEqual(self.patternLine.stateWithWall(), "RB---| <- |---")

if __name__ == '__main__':
    unittest.main()
