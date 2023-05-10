
import pytest

from Board import Game

@pytest.mark.simple
def test_init_0():
    g = Game()
    assert g.h == 6
    assert g.w == 7
    assert g.moves == []
    assert g.winner is None
    assert len(g.field) == g.h
    for row in g.field:
        assert len(row) == g.w

@pytest.mark.simple
def test_reset_0():
    g = Game()
    assert g.h == 6
    assert g.w == 7
    assert g.moves == []
    assert g.winner is None

@pytest.mark.simple
def test_reset_1():
    g = Game()
    assert len(g.field) == g.h
    for row in g.field:
        assert len(row) == g.w
        for elem in row:
            assert elem == 0

@pytest.mark.simple
def test_place_move_0():
    g = Game()
    g.place_move(0, 1)
    assert len(g.moves) == 1
    assert g.moves[0]['column'] == 0
    assert g.field[0][0] == 1
    g.place_move(0, 1)
    assert len(g.moves) == 2
    assert g.moves[-1]['column'] == 0
    assert g.field[1][0] == 1
    g.place_move(0, 1)
    g.place_move(0, 2)
    assert len(g.moves) == 4
    assert g.moves[-1]['column'] == 0
    assert g.field[3][0] == 2

@pytest.mark.edge
def test_place_move_1():
    g = Game()
    try:
        g.place_move(7, 1)
    except IndexError:
        assert True
    else:
        pytest.fail('making a move on a non-existing column')

@pytest.mark.edge
def test_place_move_2():
    g = Game()
    invalid_symbol = 3
    try:
        g.place_move(2, invalid_symbol)
    except Exception:
        assert True
    else:
        pytest.fail('only 1 and 2 are expected to be valid symbols')

@pytest.mark.simple
def test_undo_move_0():
    g = Game()
    g.place_move(5, 0)
    g.place_move(6, 1)
    g.place_move(5, 0)
    assert len(g.moves) == 3
    g.undo_move()
    assert len(g.moves) == 2
    assert g.moves[-1]['column'] == 6
    assert g.field[0][5] == 0

@pytest.mark.edge
def test_undo_move_1():
    g = Game()
    g.undo_move()
    assert True, 'undoing a move on an empty board...'

# 0 1 2 3 4 5 6 7
# . . . . . 1 . .
# . . . . . 1 . .
# . . . . . 1 . .
# . . . . . 1 . .
# . . . . . . . .
@pytest.mark.simple
def test_detect_win_at_0():
    g = Game()
    g.place_move(5, 1)
    g.place_move(5, 1)
    g.place_move(5, 1)
    g.place_move(5, 1)
    expected_symbol = 1
    assert g.detect_win_at(3, 5) == expected_symbol, 'vertical connection of 4'
    assert g.winner == 1

# 0 1 2 3 4 5 6 7
# . 2 2 2 2 . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
@pytest.mark.simple
def test_win_at_1():
    g = Game()
    g.place_move(1, 2)
    g.place_move(2, 2)
    g.place_move(3, 2)
    g.place_move(4, 2)
    expected_symbol = 2
    assert g.detect_win_at(0, 1) == expected_symbol, 'horizontal connection of 4'
    assert g.detect_win_at(0, 2) == expected_symbol
    assert g.detect_win_at(0, 3) == expected_symbol
    assert g.detect_win_at(0, 4) == expected_symbol
    assert g.detect_win_at(0, 0) == 0
    assert g.detect_win_at(0, 5) == 0


# 0 1 2 3 4 5 6 7
# . 1 2 2 2 . . .
# . . 1 2 1 . . .
# . . . 1 2 . . .
# . . . . 1 . . .
# . . . . . . . .
@pytest.mark.simple
def test_win_at_2():
    g = Game()
    g.place_move(2, 2)
    g.place_move(1, 1)
    g.place_move(3, 2)
    g.place_move(2, 1)
    g.place_move(4, 2)
    g.place_move(4, 1)
    g.place_move(3, 2)
    g.place_move(3, 1)
    g.place_move(4, 2)
    g.place_move(4, 1)
    expected_symbol = 1
    assert g.detect_win_at(0, 1) == expected_symbol, 'diagonal connection of 4'
    assert g.detect_win_at(1, 2) == expected_symbol
    assert g.detect_win_at(2, 3) == expected_symbol
    assert g.detect_win_at(3, 4) == expected_symbol
    assert g.detect_win_at(0, 2) == 0
    assert g.detect_win_at(1, 4) == 0
    assert g.detect_win_at(2, 4) == 0
    assert g.detect_win_at(4, 5) == 0


# 0 1 2 3 4 5 6 7
# 1 1 1 2 2 . . .
# 1 1 2 2 . . . .
# 1 1 2 . . . . .
# 2 2 . . . . . .
# 2 . . . . . . .
@pytest.mark.simple
def test_win_at_3():
    g = Game()
    g.place_move(0, 1)  # top left triangle
    g.place_move(0, 1)
    g.place_move(0, 1)
    g.place_move(1, 1)
    g.place_move(1, 1)
    g.place_move(2, 1)

    g.place_move(3, 2)  # another diagonal
    g.place_move(2, 2)
    g.place_move(1, 1)
    g.place_move(0, 2)

    g.place_move(0, 2)  # finishing diagonal
    g.place_move(1, 2)
    g.place_move(3, 2)
    g.place_move(4, 2)

    assert g.detect_win_at(4, 0) == 0, 'this lines has not won anything yet'
    assert g.detect_win_at(3, 1) == 0
    assert g.detect_win_at(2, 2) == 0
    assert g.detect_win_at(1, 3) == 0
    assert g.detect_win_at(0, 4) == 0
    assert g.detect_win_at(1, 1) == 0

    g.place_move(2, 2)  # winning move

    assert g.detect_win_at(4, 0) == 2, 'now there is a winning line with 5 symbols'
    assert g.detect_win_at(3, 1) == 2
    assert g.detect_win_at(2, 2) == 2
    assert g.detect_win_at(1, 3) == 2
    assert g.detect_win_at(0, 4) == 2
    assert g.detect_win_at(1, 1) == 0
