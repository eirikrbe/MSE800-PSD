"""Unit tests for the Tic-tac-toe game in main.py."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from main import Board, ConsoleMoveProvider, ConsoleView


class TestWinDetection(unittest.TestCase):
    """Tests for detecting winning board states."""

    def test_row_win(self) -> None:
        """A full top row of one mark is a win."""
        board = Board()
        for position in (1, 2, 3):
            board.place(position, "X")
        self.assertEqual(board.winner(), "X")

    def test_column_win(self) -> None:
        """A full left column of one mark is a win."""
        board = Board()
        for position in (1, 4, 7):
            board.place(position, "O")
        self.assertEqual(board.winner(), "O")

    def test_diagonal_win(self) -> None:
        """A full diagonal of one mark is a win."""
        board = Board()
        for position in (1, 5, 9):
            board.place(position, "X")
        self.assertEqual(board.winner(), "X")

    def test_no_winner(self) -> None:
        """An empty board has no winner."""
        board = Board()
        self.assertIsNone(board.winner())


class TestDrawDetection(unittest.TestCase):
    """Tests for detecting a full board and a draw outcome."""

    def test_board_full(self) -> None:
        """A board with every cell marked reports as full."""
        board = Board()
        marks = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        for index, mark in enumerate(marks, start=1):
            board.place(index, mark)
        self.assertTrue(board.is_full())

    def test_draw_has_no_winner(self) -> None:
        """A full board with no line filled has no winner."""
        board = Board()
        marks = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        for index, mark in enumerate(marks, start=1):
            board.place(index, mark)
        self.assertIsNone(board.winner())

    def test_not_full_when_empty(self) -> None:
        """A fresh board is not full."""
        board = Board()
        self.assertFalse(board.is_full())


class TestInvalidMoveHandling(unittest.TestCase):
    """Tests for rejecting bad input in get_move and is_free."""

    def test_occupied_cell_not_free(self) -> None:
        """A marked cell is reported as not free."""
        board = Board()
        board.place(5, "X")
        self.assertFalse(board.is_free(5))
        self.assertTrue(board.is_free(1))

    def test_prompt_rejects_then_accepts(self) -> None:
        """get_move loops past bad input and returns a valid move."""
        board = Board()
        board.place(3, "X")
        mover = ConsoleMoveProvider()
        inputs = ["abc", "0", "10", "3", "7"]
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(io.StringIO()):
                position = mover.get_move(board, "O")
        self.assertEqual(position, 7)

    def test_prompt_messages_for_bad_input(self) -> None:
        """Each kind of bad input produces an error message."""
        board = Board()
        board.place(4, "O")
        mover = ConsoleMoveProvider()
        inputs = ["x", "99", "4", "1"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                position = mover.get_move(board, "X")
        text = output.getvalue()
        self.assertEqual(position, 1)
        self.assertIn("1 to 9", text)
        self.assertIn("already taken", text)


class TestBoardDisplay(unittest.TestCase):
    """Tests for the textual rendering of the board."""

    def test_empty_board_output(self) -> None:
        """An empty board shows cells numbered 1 through 9."""
        text = ConsoleView().render(Board())
        for number in range(1, 10):
            self.assertIn(str(number), text)
        self.assertIn("---+---+---", text)

    def test_marks_appear_in_output(self) -> None:
        """Placed marks are visible in the rendered board."""
        board = Board()
        board.place(1, "X")
        board.place(9, "O")
        text = ConsoleView().render(board)
        self.assertIn("X", text)
        self.assertIn("O", text)


if __name__ == "__main__":
    unittest.main()
