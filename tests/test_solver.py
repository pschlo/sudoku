import pytest

from sudoku_solver import InvalidSudokuError, UnsolvableSudokuError, solve_sudoku


PUZZLE = [
    [4, 1, 0, 0, 6, 5, 0, 0, 7],
    [0, 0, 6, 0, 0, 7, 4, 8, 0],
    [2, 0, 7, 4, 9, 0, 0, 0, 6],
    [0, 6, 0, 0, 7, 0, 1, 0, 0],
    [3, 0, 1, 5, 0, 0, 0, 7, 2],
    [0, 9, 0, 0, 4, 2, 3, 0, 8],
    [1, 0, 8, 6, 0, 0, 0, 2, 9],
    [0, 2, 0, 0, 1, 8, 6, 4, 0],
    [6, 0, 0, 3, 0, 0, 0, 1, 0],
]


def test_solves_puzzle_without_mutating_input() -> None:
    original = [row.copy() for row in PUZZLE]

    solved = solve_sudoku(PUZZLE)

    assert PUZZLE == original
    assert all(set(row) == set(range(1, 10)) for row in solved)
    assert all(
        set(solved[row][column] for row in range(9)) == set(range(1, 10)) for column in range(9)
    )
    assert all(
        {solved[box_row + row][box_column + column] for row in range(3) for column in range(3)}
        == set(range(1, 10))
        for box_row in range(0, 9, 3)
        for box_column in range(0, 9, 3)
    )
    assert all(
        not value or solved[row][column] == value
        for row, puzzle_row in enumerate(PUZZLE)
        for column, value in enumerate(puzzle_row)
    )


@pytest.mark.parametrize(
    "puzzle",
    [
        [[0] * 9 for _ in range(8)],
        [[0] * 9 for _ in range(8)] + [[0] * 8],
        [[0] * 9 for _ in range(8)] + [[0] * 8 + [10]],
        [[1, 1] + [0] * 7] + [[0] * 9 for _ in range(8)],
    ],
)
def test_rejects_invalid_puzzles(puzzle: list[list[int]]) -> None:
    with pytest.raises(InvalidSudokuError):
        solve_sudoku(puzzle)


def test_reports_unsolvable_puzzle() -> None:
    puzzle = [
        [1, 2, 3, 4, 5, 6, 7, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        *[[0] * 9 for _ in range(7)],
    ]

    with pytest.raises(UnsolvableSudokuError):
        solve_sudoku(puzzle)
