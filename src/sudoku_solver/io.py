from __future__ import annotations

from pathlib import Path

from .solver import Grid, InvalidSudokuError, validate_sudoku


def parse_sudoku(text: str) -> Grid:
    """Parse nine compact or whitespace-separated rows of Sudoku values."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) != 9:
        raise InvalidSudokuError("A Sudoku file must contain exactly 9 non-empty rows")

    rows: Grid = []
    for line in lines:
        values = line.split() if any(character.isspace() for character in line) else list(line)
        if len(values) != 9 or any(len(value) != 1 or not value.isdigit() for value in values):
            raise InvalidSudokuError("Each Sudoku row must contain exactly 9 digits")
        rows.append([int(value) for value in values])
    return validate_sudoku(rows)


def format_sudoku(puzzle: Grid) -> str:
    """Serialize a Sudoku using the repository's space-separated format."""
    grid = validate_sudoku(puzzle)
    return "\n".join(" ".join(map(str, row)) for row in grid) + "\n"


def load_sudoku(path: Path) -> Grid:
    return parse_sudoku(path.read_text(encoding="utf-8"))


def save_sudoku(path: Path, puzzle: Grid) -> None:
    path.write_text(format_sudoku(puzzle), encoding="utf-8")
