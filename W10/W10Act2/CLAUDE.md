# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A two-player, terminal-based Tic-tac-toe game (MSE800-PSD coursework, Week 10
Activity 2). Pure standard-library Python 3, no third-party runtime
dependencies.

## Commands

Run the game:

```bash
python3 main.py
```

Run the full test suite (verbose):

```bash
python3 -m unittest test_tictactoe.py -v
```

Run a single test class or method:

```bash
python3 -m unittest test_tictactoe.TestWinDetection -v
python3 -m unittest test_tictactoe.TestWinDetection.test_row_win -v
```

Lint (the project is held to a clean flake8 run and a 10.00/10 pylint score):

```bash
python3 -m flake8 main.py
python3 -m pylint main.py
```

## Code style

Strict PEP 8 is a project requirement, not just a convention: 79-char line
limit, snake_case, type hints on every function signature, and a docstring on
every module, class, and function. Keep `main.py` at flake8-clean / pylint
10.00 when editing.

## Architecture

The design follows SOLID principles: state, input, output, and match flow are
each isolated in their own type, and `Game` depends only on abstractions.

- `main.py` — six types across four responsibilities:
  - `Board` — **pure state and rules**, no I/O. Cells are a flat `List[str]`
    of length 9, all initialised to the `Board.EMPTY` sentinel (`" "`).
    **Positions are 1-based** in the public API (`is_free`, `place`); the class
    converts to 0-based internally. `winner()` scans the 8 line index-triples
    in `Board.LINES` and **must guard against `EMPTY`** — three blank cells
    share a value, so without the guard an empty line would register as a win.
    `is_full()` treats a cell as occupied when it is not `EMPTY`. The `1`..`9`
    labels are NOT stored; they are applied at render time only.
  - `MoveProvider` (ABC) / `ConsoleMoveProvider` — **input**. `get_move(board,
    player)` runs the validation loop (digit check, 1–9 range, `board.is_free`)
    and returns a valid 1-based position. Swap in another subclass (AI,
    scripted) without touching `Game`.
  - `GameView` (ABC) / `ConsoleView` — **output**. `show_board()` and
    `announce()` are the abstract surface; `ConsoleView.render(board)` builds
    the printable string and is where the `1`..`9` labels are substituted for
    empty cells. Input and output are deliberately separate interfaces.
  - `Game` — **match flow only**: player rotation (`current` toggles via
    `1 - self.current`) and the win/draw loop in `play()`. It receives a
    `GameView` and a `MoveProvider` through its constructor (defaulting to the
    console implementations), so it depends on abstractions, never on
    `input()`/`print()` directly.
  - `main()` is the entry point, guarded by `if __name__ == "__main__"`. It
    wraps `Game().play()` in a play-again loop.
  - The two single-method abstractions carry a
    `# pylint: disable=too-few-public-methods` — the standard idiom for
    interface/strategy classes, needed to keep the 10.00 score.

- `test_tictactoe.py` — unittest suite, four `TestCase` classes mirroring the
  four required coverage areas (win detection, draw detection, invalid-move
  handling, board display).

## Testing the interactive parts

`ConsoleMoveProvider.get_move()` and `ConsoleView` do console I/O. Tests cover
them without a real terminal by constructing the concrete classes directly —
the abstractions make them substitutable in isolation:

- Mock input with `patch("builtins.input", side_effect=[...])`, supplying a
  list of strings with bad entries followed by a valid one to exercise the
  validation loop in `get_move()`.
- For output, prefer asserting on the string returned by
  `ConsoleView().render(board)`. Use `contextlib.redirect_stdout(io.StringIO())`
  only to silence prompt noise during input tests.

When adding a new input source or output target, add a `MoveProvider` /
`GameView` subclass and inject it — do not fold I/O back into `Board` or
`Game`.
