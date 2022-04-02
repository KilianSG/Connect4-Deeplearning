from unittest import TestCase
from agents.common import Board, GameState
import numpy


class TestBoard(TestCase):
    def test_apply_player_move(self):
        board = Board()
        board2 = Board()

        self.assertTrue((board.board == board2.board).all(), "Initializing of board gone wrong")
        board.apply_player_move(0, 1, False)

        self.assertFalse((board.board == board2.board).all(), "Board Piece not placed in first Row")
        board2.apply_player_move(0, 1, False)

        self.assertTrue((board.board == board2.board).all(), "both Boards should have the same state")
        check = numpy.asarray([[1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])

        self.assertTrue((board.board == check).all())

        for times in range(5):
            board.apply_player_move(0, 1, False)
            board2.apply_player_move(0, 2, False)

        check = numpy.asarray(
            [[1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0]])
        self.assertTrue((board.board == check).all(), "Column 1 wrongly filled")
        self.assertFalse((board.board == board2.board).all(), "Wrong Pieces Placed or no Pieces placed.")

        for times in range(6):
            board.apply_player_move(6, 2, False)
        check = numpy.asarray(
            [[1, 0, 0, 0, 0, 0, 2], [1, 0, 0, 0, 0, 0, 2], [1, 0, 0, 0, 0, 0, 2], [1, 0, 0, 0, 0, 0, 2],
             [1, 0, 0, 0, 0, 0, 2], [1, 0, 0, 0, 0, 0, 2]])
        self.assertTrue((board.board == check).all(), "Column 7 wrongly filled")
        for times in range(5):
            board.apply_player_move(times+1, (times % 2)+1, False)
        check = numpy.asarray(
            [[1, 1, 2, 1, 2, 1, 2], [1, 0, 0, 0, 0, 0, 2], [1, 0, 0, 0, 0, 0, 2], [1, 0, 0, 0, 0, 0, 2],
             [1, 0, 0, 0, 0, 0, 2], [1, 0, 0, 0, 0, 0, 2]])
        self.assertTrue((board.board == check).all(), "Row 1 wrongly filled")
        check = numpy.asarray(
            [[1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 2, 1, 2],
             [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 2, 1, 2]])
        for rows in range(5):
            for column in range(5):
                board.apply_player_move(column + 1, (column % 2) + 1, False)
        self.assertTrue((board.board == check).all(), "Row 6 wrongly filled")

    def test_take_back_player_move(self):
        board = Board()
        board2 = Board()
        board2.take_back_player_move(3, 1)
        self.assertTrue((board.board == board2.board).all(), "take_back_player_move changed Board")

        board.apply_player_move(0, 1, False)
        check = numpy.asarray(
            [[1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
        self.assertTrue((board.board == check).all(), "Error in apply_player_move")
        successful = board.take_back_player_move(0, 1)
        self.assertTrue(successful, "take_back_player_move should have succeeded")
        self.assertFalse((board.board == check).all(), "Board should have changed")

        board.apply_player_move(0, 1, False)
        wrong = board.take_back_player_move(0, 2)
        self.assertTrue((board.board == check).all(), "Board shouldn't have changed")
        self.assertFalse(wrong, "take_back_player_move should have failed")

        for how_often in range(3):
            board.apply_player_move(0, 1, False)
        for how_often in range(3):
            board.take_back_player_move(0, 1)
        successful = board.take_back_player_move(0, 1)
        self.assertTrue(successful, "take_back_player_move should have succeeded")

        wrong = board.take_back_player_move(0, 1)
        self.assertFalse(wrong, "take_back_player_move should have failed")

        wrong = board.take_back_player_move(0, 2)
        self.assertFalse(wrong, "take_back_player_move should have failed in 1 Column")

        for how_often in range(6):
            board.apply_player_move(0, 1, False)
        board.take_back_player_move(0, 1)
        check = numpy.asarray(
            [[1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
        self.assertTrue((board.board == check).all(), "take_back_player_move failed in 1 Column")

        for how_often in range(6):
            board.apply_player_move(6, 1, False)
        board.take_back_player_move(6, 1)
        check = numpy.asarray(
            [[1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0]])
        self.assertTrue((board.board == check).all(), "take_back_player_move failed in 7 Column")

    def test_get_possible_moves(self):
        board = Board()
        for row in range(7):
            for column in range(6):
                board.apply_player_move(row, 1)
        check = numpy.asarray(
            [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]])
        self.assertTrue((board.board == check).all(), "Error in apply_player_move")

        check = [-1, -1, -1, -1, -1, -1, -1]
        self.assertTrue((board.get_possible_moves() == check), "wrong possible turns returned(empty)")

        check = numpy.asarray(
            [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1]])
        board.take_back_player_move(0, 1)
        self.assertTrue((board.board == check).all(), "Error in take_back_player_move")

        check = [0, -1, -1, -1, -1, -1, -1]
        self.assertTrue((board.get_possible_moves() == check), "wrong possible turns returned(one item)")

        check = [0, -1, -1, -1, -1, -1, 6]
        board.take_back_player_move(6, 1)
        self.assertTrue((board.get_possible_moves() == check), "wrong possible turns returned(two item)")

        check = [0, -1, -1, 3, -1, -1, 6]
        board.take_back_player_move(3, 1)
        self.assertTrue((board.get_possible_moves() == check), "wrong possible turns returned(three item)")

        check = [0, 1, -1, 3, -1, -1, 6]
        board.take_back_player_move(1, 1)
        self.assertTrue((board.get_possible_moves() == check), "wrong possible turns returned(4)")

        check = [0, 1, 2, 3, -1, -1, 6]
        board.take_back_player_move(2, 1)
        self.assertTrue((board.get_possible_moves() == check), "wrong possible turns returned(5)")

        check = [0, 1, 2, 3, 4, -1, 6]
        board.take_back_player_move(4, 1)
        self.assertTrue((board.get_possible_moves() == check), "wrong possible turns returned(6)")

        check = [0, 1, 2, 3, 4, 5, 6]
        board.take_back_player_move(5, 1)
        self.assertTrue((board.get_possible_moves() == check), "wrong possible turns returned(7)")

    def test_is_won(self):
        board = Board()
        for column in range(3):
            board.apply_player_move(column, 1)
            for row in range(column):
                board.apply_player_move(column, 1)
        check = numpy.asarray(
            [[1, 1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
        self.assertTrue((board.board == check).all(), "Error in apply_player_move")
        self.assertFalse(board.is_won(1))
        self.assertFalse(board.is_won(2))

        board.apply_player_move(2, 2)
        self.assertFalse(board.is_won(1))
        self.assertFalse(board.is_won(2))

        board.take_back_player_move(2, 2)
        check = numpy.asarray(
            [[1, 1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
        self.assertTrue((board.board == check).all(), "Error in take_back_player_move")

        board.apply_player_move(2, 1)
        self.assertTrue(board.is_won(1), "Didn't see win horizontal")
        self.assertFalse(board.is_won(2), "Mixed up winner")

        board.take_back_player_move(2, 1)
        self.assertFalse(board.is_won(1))

        board.apply_player_move(3, 1)
        self.assertTrue(board.is_won(1), "Didn't see win Vertical")
        self.assertFalse(board.is_won(2), "Mixed up winner")

        board.take_back_player_move(3, 1)
        board.apply_player_move(3, 2)
        self.assertFalse(board.is_won(1))
        self.assertFalse(board.is_won(2))

        board.apply_player_move(3, 1)
        board.apply_player_move(3, 1)
        board.apply_player_move(3, 1)
        self.assertTrue(board.is_won(1), "Didn't see win from bottom-left to top-right")
        self.assertFalse(board.is_won(2), "Mixed up winner")

        board = Board()
        for column in reversed(range(4, 7)):
            board.apply_player_move(column, 2)
            for row in reversed(range(6-column)):
                board.apply_player_move(column, 2)
        board.apply_player_move(3, 2)
        self.assertTrue(board.is_won(2), "Didn't see win horizontal(2)")
        self.assertFalse(board.is_won(1), "Mixed up winner")

        board.take_back_player_move(3, 2)
        board.apply_player_move(3, 1)
        board.apply_player_move(3, 2)
        board.apply_player_move(3, 2)
        board.apply_player_move(3, 2)
        self.assertTrue(board.is_won(2), "Didn't see win from top-left to bottom-right")
        self.assertFalse(board.is_won(1), "Mixed up winner")

        board.take_back_player_move(3, 2)
        board.apply_player_move(0, 2)
        board.apply_player_move(1, 2)
        self.assertFalse(board.is_won(2), "Win went through wall")
        self.assertFalse(board.is_won(1), "Mixed up winner")

        board.take_back_player_move(3, 2)
        for full_aside_of_top in range(4):
            board.apply_player_move(6, 2)
        board.apply_player_move(6, 1)
        board.apply_player_move(5, 2)
        board.apply_player_move(5, 2)
        board.apply_player_move(5, 1)
        board.apply_player_move(4, 1)
        board.apply_player_move(3, 1)
        self.assertTrue(board.is_won(1), "Win diagonal, didn't reach top-right")
        board.take_back_player_move(4, 1)
        board.apply_player_move(0, 2)
        for x in range(3):
            board.apply_player_move(2, 2)
            board.apply_player_move(1, 2)
            board.apply_player_move(0, 2)
        board.apply_player_move(2, 1)
        board.apply_player_move(1, 1)
        self.assertFalse(board.is_won(1))
        board.apply_player_move(0, 1)
        self.assertTrue(board.is_won(1), "Win diagonal, didn't reach top-left")

    def test_get_pretty_print_board(self):
        board = Board()
        check = "|===============|\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "|===============|\n" \
                "| 0 1 2 3 4 5 6 |"
        self.assertTrue(check == board.get_pretty_print_board(), "Board looks different")

        board.apply_player_move(0, 1)
        check = "|===============|\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "| X             |\n" \
                "|===============|\n" \
                "| 0 1 2 3 4 5 6 |"
        self.assertTrue(check == board.get_pretty_print_board(), "Wrongly printed Player1")

        board.apply_player_move(1, 2)
        check = "|===============|\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "|               |\n" \
                "| X O           |\n" \
                "|===============|\n" \
                "| 0 1 2 3 4 5 6 |"
        self.assertTrue(check == board.get_pretty_print_board(), "Wrongly printed Player2")

        board = Board()
        for row in range(6):
            for column in range(7):
                board.apply_player_move(column, 1)
        check = "|===============|\n" \
                "| X X X X X X X |\n" \
                "| X X X X X X X |\n" \
                "| X X X X X X X |\n" \
                "| X X X X X X X |\n" \
                "| X X X X X X X |\n" \
                "| X X X X X X X |\n" \
                "|===============|\n" \
                "| 0 1 2 3 4 5 6 |"
        self.assertTrue(check == board.get_pretty_print_board(), "Wrong fully filled board")

    def test_copy_board(self):
        board1 = Board()
        board2 = board1.copy_board()
        self.assertTrue((board1.board == board2.board).all())
        board1.apply_player_move(2, 1)
        self.assertFalse((board1.board == board2.board).all())

    def test_evaluation(self):
        board = Board()
        board.apply_player_move(3, 1)
        board.apply_player_move(2, 1)
        board.apply_player_move(4, 1)
        board.apply_player_move(0, 2)
        board.apply_player_move(0, 2)
        board.apply_player_move(0, 2)
        self.assertTrue(board.evaluation(1) > board.evaluation(2))

        board = Board()
        board.apply_player_move(3, 1)
        board.apply_player_move(2, 1)
        board.apply_player_move(4, 2)
        board.apply_player_move(0, 2)
        board.apply_player_move(0, 2)
        board.apply_player_move(0, 1)
        self.assertTrue(board.evaluation(1) > board.evaluation(2))

    def test_get_game_state(self):
        board = Board()
        board.apply_player_move(3, 2)
        board.apply_player_move(2, 2)
        board.apply_player_move(4, 2)
        board.apply_player_move(1, 2)
        self.assertTrue(board.get_game_state() == -1)

        board = Board()
        board.apply_player_move(3, 1)
        board.apply_player_move(2, 1)
        board.apply_player_move(4, 1)
        board.apply_player_move(1, 1)
        self.assertTrue(board.get_game_state() == 1)

        board = Board()
        self.assertTrue(board.get_game_state() == GameState.STILL_PLAYING)




