from __future__ import annotations

from collections.abc import Sequence
from numbers import Integral


GRID_SIZE = 9
BOX_SIZE = 3
Grid = list[list[int]]


class SudokuError(ValueError):
    """Base class for Sudoku validation and solving errors."""


class InvalidSudokuError(SudokuError):
    """Raised when a puzzle has an invalid shape, value, or duplicate."""


class UnsolvableSudokuError(SudokuError):
    """Raised when a valid puzzle has no solution."""


def validate_sudoku(puzzle: Sequence[Sequence[int]]) -> Grid:
    """Validate a puzzle and return it as an independent mutable grid."""
    if len(puzzle) != GRID_SIZE or any(len(row) != GRID_SIZE for row in puzzle):
        raise InvalidSudokuError("A Sudoku must contain exactly 9 rows of 9 values")

    grid: Grid = []
    for row in puzzle:
        normalized_row: list[int] = []
        for value in row:
            if isinstance(value, bool) or not isinstance(value, Integral):
                raise InvalidSudokuError("Sudoku values must be integers from 0 to 9")
            normalized_value = int(value)
            if not 0 <= normalized_value <= GRID_SIZE:
                raise InvalidSudokuError("Sudoku values must be integers from 0 to 9")
            normalized_row.append(normalized_value)
        grid.append(normalized_row)

    units = list(grid)
    units.extend([[grid[row][column] for row in range(GRID_SIZE)] for column in range(GRID_SIZE)])
    units.extend(
        [
            [
                grid[box_row + row][box_column + column]
                for row in range(BOX_SIZE)
                for column in range(BOX_SIZE)
            ]
            for box_row in range(0, GRID_SIZE, BOX_SIZE)
            for box_column in range(0, GRID_SIZE, BOX_SIZE)
        ]
    )
    for unit in units:
        filled = [value for value in unit if value]
        if len(filled) != len(set(filled)):
            raise InvalidSudokuError("The puzzle contains a duplicate value")

    return grid


def solve_sudoku(puzzle: Sequence[Sequence[int]]) -> Grid:
    """Return a solved copy of a valid Sudoku puzzle."""
    grid = validate_sudoku(puzzle)

    def candidates(row: int, column: int) -> set[int]:
        used = set(grid[row])
        used.update(grid[index][column] for index in range(GRID_SIZE))
        box_row = row // BOX_SIZE * BOX_SIZE
        box_column = column // BOX_SIZE * BOX_SIZE
        used.update(
            grid[box_row + row_offset][box_column + column_offset]
            for row_offset in range(BOX_SIZE)
            for column_offset in range(BOX_SIZE)
        )
        return set(range(1, GRID_SIZE + 1)) - used

    def fill_next_cell() -> bool:
        target: tuple[int, int] | None = None
        target_candidates: set[int] | None = None

        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                if grid[row][column] != 0:
                    continue
                possible = candidates(row, column)
                if not possible:
                    return False
                if target_candidates is None or len(possible) < len(target_candidates):
                    target = (row, column)
                    target_candidates = possible
                    if len(possible) == 1:
                        break
            if target_candidates is not None and len(target_candidates) == 1:
                break

        if target is None or target_candidates is None:
            return True

        row, column = target
        for value in sorted(target_candidates):
            grid[row][column] = value
            if fill_next_cell():
                return True
        grid[row][column] = 0
        return False

    if not fill_next_cell():
        raise UnsolvableSudokuError("This Sudoku has no solution")
    return grid
