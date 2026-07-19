from pathlib import Path

import pytest

from sudoku_solver import InvalidSudokuError, load_sudoku, parse_sudoku, save_sudoku


COMPACT_PUZZLE = """\
410065007
006007480
207490006
060070100
301500072
090042308
108600029
020018640
600300010
"""


def test_parses_compact_and_space_separated_files() -> None:
    compact = parse_sudoku(COMPACT_PUZZLE)
    spaced = parse_sudoku(COMPACT_PUZZLE.replace("", " ").strip())

    assert compact == spaced
    assert compact[0] == [4, 1, 0, 0, 6, 5, 0, 0, 7]


def test_file_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "puzzle.sd"
    puzzle = parse_sudoku(COMPACT_PUZZLE)

    save_sudoku(path, puzzle)

    assert load_sudoku(path) == puzzle


@pytest.mark.parametrize("text", ["", "123", "\n".join(["000000000"] * 8)])
def test_rejects_invalid_file_format(text: str) -> None:
    with pytest.raises(InvalidSudokuError):
        parse_sudoku(text)
