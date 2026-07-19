# Sudoku Solver

A small graphical Sudoku solver.

## Run

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), open a terminal in this directory, and run:

```console
uv run sudoku
```

Enter digits with the keyboard, move with the arrow keys, and press Enter to solve the puzzle. Use **Open** to load one of the examples in the `sudokus` directory.

Puzzle files contain nine rows of digits. Use `0` for an empty cell; spaces between digits are optional.

## Development

```console
uv run pytest
uv build
```
