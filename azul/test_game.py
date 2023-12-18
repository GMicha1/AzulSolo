from __future__ import annotations
from typing import List
from game import Game
from customErrors import NotPlayersTurn, GameIsOver, EmptySourceOrWrongColour, NonViableColorIdx
from interfaces import FinishRoundResult
from simple_types import Tile, RED, STARTING_PLAYER, Points
import unittest
from unittest.mock import Mock


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game: Game = Game(3,["A", "B"], 2)

    def test_game(self) -> None:
        self.assertFalse(self.game.gameOver)
        self.assertEqual(self.game.currentPlayer, 2)
        self.assertEqual(self.game.nextFirst, 2)
        self.assertEqual(len(self.game._playerBoards), 3)

        ##trying out mocktests instead pf fake classes
        self.game._table.take = Mock(return_value = [])
        self.game._table.take = Mock(return_value = [RED, RED, RED])
        self.game._table.isRoundEnd = Mock(return_value = False)
        self.game._table.state = Mock(return_value="Table state")
        self.game.bag.state = Mock(return_value="Bag state")
        self.game._observer.notifyEverybody = Mock()
        for i in self.game._playerBoards:
            i.put = Mock()
            i.finishRound = Mock(return_value = FinishRoundResult.NORMAL)
            i.state = Mock(return_value = "Board state of: " + i._player_name)
            i.endGame = Mock()
            for j in i._pattern_line:
                j.stateWithWall = Mock(return_value = "pattern line state")
            i._floor.state = Mock(return_value = "floor state")
        
        with self.assertRaises(NonViableColorIdx):
            self.game.takeTiles(2, 3, 0)

        takenTiles0: List[Tile] = self.game.takeTiles(2, -1, 1)
        self.assertEqual(takenTiles0, [RED, RED, RED])
        self.assertEqual(self.game.nextFirst, 2)
        
        self.game.putTiles(takenTiles0, 0)
        self.game._playerBoards[2].put.assert_called_with(0, [RED, RED, RED])
        self.assertEqual(self.game.nextFirst, 2)
        self.assertEqual(self.game.currentPlayer, 0)
        
        boardState: str = "\npattern line state"*5 + "\nfloor state\n"
        self.assertEqual(self.game.state(), "\nThis player takes tiles next:"
                         +"\nBoard state of: A" + boardState
                         +"\nBoard state of: B" + boardState
                         +"\nBoard state of: "+ boardState)
        self.assertEqual(self.game.stateTable(), "Table state\nBag state\n")

        self.game._table.startNewRound = Mock()
        self.game._table.tableCenter.startNewRound = Mock()
        self.game.startNewRound()
        self.game._table.startNewRound.assert_called_once_with()
        self.game._table.tableCenter.startNewRound.assert_called_once_with()

        self.game.startNewRound = Mock()
        self.game.finishRound()
        self.game._observer.notifyEverybody.assert_called_once_with("Starting new round... \n")

        with self.assertRaises(NotPlayersTurn):
            self.game.take(1, 2, 3, 4)
            
        with self.assertRaises(ValueError):
            self.game.take(0, -2, 3, 4)
            
        with self.assertRaises(NonViableColorIdx):
            self.game.take(0, 2, 7, 4)
            
        with self.assertRaises(NonViableColorIdx):
            self.game.take(0, 2, -3, 4)

        self.game._table.take = Mock(return_value = [])
        with self.assertRaises(EmptySourceOrWrongColour):
            self.game.take(0, 2, 3, 4)


        self.game._table.take = Mock(return_value = [STARTING_PLAYER, RED])
        self.game.take(0, 0, 1, 2)
        self.assertEqual(self.game.nextFirst, 0)
        self.assertEqual(self.game.currentPlayer, 1)

        self.game._table.take = Mock(return_value = [RED, RED])
        self.game._table.isRoundEnd = Mock(return_value = True)
        self.game.take(1, 0, 1, 2)
        self.game.startNewRound.assert_called_with()
        self.assertFalse(self.game.gameOver)
        self.assertEqual(self.game.currentPlayer, 0) #changed to nextFirst instead of +1

        self.game._playerBoards[2].finishRound = Mock(return_value=FinishRoundResult.GAME_FINISHED)
        self.game.take(0, 1, 1, 1)
        self.game._playerBoards[0].endGame.assert_called_once_with()
        self.game._playerBoards[1].endGame.assert_called_once_with()
        assert not self.game._playerBoards[2].endGame.called
        self.assertTrue(self.game.gameOver)
        
        self.assertTrue("\nThis player takes tiles next:" not in self.game.state())

        with self.assertRaises(GameIsOver):
            self.game.take(0, 1, 1, 1)

        self.game._playerBoards[1]._points = Points(12)
        self.game.finishRound()
        self.game._observer.notifyEverybody.assert_called_with("The winner is B with 12 points!")


if __name__ == '__main__':
    unittest.main()
