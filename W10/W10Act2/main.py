"""A two-player Tic-tac-toe game played in the terminal."""

from abc import ABC, abstractmethod
from typing import List, Optional


class Board:
    """Hold the 3x3 grid state and answer questions about it."""

    EMPTY: str = " "
    LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    def __init__(self) -> None:
        """Initialise an empty board of nine blank cells."""
        self.cells: List[str] = [Board.EMPTY] * 9

    def is_free(self, position: int) -> bool:
        """Return True if the given 1-based cell is unoccupied."""
        return self.cells[position - 1] == Board.EMPTY

    def place(self, position: int, mark: str) -> None:
        """Place a player's mark on the given 1-based cell."""
        self.cells[position - 1] = mark

    def winner(self) -> Optional[str]:
        """Return the winning mark, or None if there is no winner."""
        for a, b, c in Board.LINES:
            if self.cells[a] != Board.EMPTY and \
                    self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def is_full(self) -> bool:
        """Return True if every cell has been marked."""
        return all(cell != Board.EMPTY for cell in self.cells)


class MoveProvider(ABC):  # pylint: disable=too-few-public-methods
    """Abstract source of the next move for a player."""

    @abstractmethod
    def get_move(self, board: Board, player: str) -> int:
        """Return a valid 1-based cell choice for the given player."""


class GameView(ABC):
    """Abstract output channel for the game."""

    @abstractmethod
    def show_board(self, board: Board) -> None:
        """Display the current state of the board."""

    @abstractmethod
    def announce(self, message: str) -> None:
        """Display a single message to the players."""


class ConsoleMoveProvider(MoveProvider):
    # pylint: disable=too-few-public-methods
    """Read and validate a move from the terminal."""

    def get_move(self, board: Board, player: str) -> int:
        """Prompt until the player enters a free cell, then return it."""
        while True:
            choice = input(f"Player {player}, choose a cell (1-9): ")
            if not choice.isdigit():
                print("Please enter a number from 1 to 9.")
                continue
            position = int(choice)
            if position < 1 or position > 9:
                print("Please enter a number from 1 to 9.")
                continue
            if not board.is_free(position):
                print("That cell is already taken.")
                continue
            return position


class ConsoleView(GameView):
    """Render the board and messages to the terminal."""

    def render(self, board: Board) -> str:
        """Return the board as a printable string, numbering free cells."""
        labels = [
            cell if cell != Board.EMPTY else str(index + 1)
            for index, cell in enumerate(board.cells)
        ]
        rows = [labels[i:i + 3] for i in range(0, 9, 3)]
        parts = [""]
        for index, row in enumerate(rows):
            parts.append(" " + " | ".join(row) + " ")
            if index < 2:
                parts.append("---+---+---")
        parts.append("")
        return "\n".join(parts)

    def show_board(self, board: Board) -> None:
        """Print the rendered board to the console."""
        print(self.render(board))

    def announce(self, message: str) -> None:
        """Print a message to the console."""
        print(message)


class Game:
    """Coordinate match flow between two players."""

    def __init__(
        self,
        view: Optional[GameView] = None,
        mover: Optional[MoveProvider] = None,
    ) -> None:
        """Set up a game, defaulting to console input and output."""
        self.board: Board = Board()
        self.players: List[str] = ["X", "O"]
        self.current: int = 0
        self.view: GameView = view if view is not None else ConsoleView()
        self.mover: MoveProvider = (
            mover if mover is not None else ConsoleMoveProvider()
        )

    def current_player(self) -> str:
        """Return the mark of the player whose turn it is."""
        return self.players[self.current]

    def switch_player(self) -> None:
        """Advance the turn to the other player."""
        self.current = 1 - self.current

    def play(self) -> None:
        """Run the main game loop until a win or a draw occurs."""
        self.view.announce("Welcome to Tic-tac-toe!")
        self.view.show_board(self.board)
        while True:
            player = self.current_player()
            position = self.mover.get_move(self.board, player)
            self.board.place(position, player)
            self.view.show_board(self.board)
            winner = self.board.winner()
            if winner is not None:
                self.view.announce(f"Player {winner} wins!")
                break
            if self.board.is_full():
                self.view.announce("It's a draw!")
                break
            self.switch_player()


def main() -> None:
    """Play games repeatedly until the player chooses to stop."""
    while True:
        game = Game()
        game.play()
        choice = input("Do you want play another game (y/n)?: ").lower()
        if choice != "y":
            print("Program finished.")
            break


if __name__ == "__main__":
    main()
