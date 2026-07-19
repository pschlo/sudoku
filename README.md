# Sudoku Solver

A small graphical Sudoku solver.

## Run

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run:

```console
uvx --from https://github.com/pschlo/sudoku/archive/refs/heads/master.zip sudoku
```

Enter digits with the keyboard, move with the arrow keys, and press Enter to solve the puzzle. Use **Open** to load one of the examples in the `sudokus` directory.

Puzzle files contain nine rows of digits. Use `0` for an empty cell; spaces between digits are optional.

## Development

```console
uv sync --locked
uv run sudoku
uv run pytest
uv build
```
