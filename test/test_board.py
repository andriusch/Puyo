from puyo.board import *
from nose.tools import *
import pygame
pygame.init()

class TestBoardCommon(object):
    def add_puyo(self, color, row, col):
        puyo = Puyo(self.subject, color)
        puyo.x = col * 64
        puyo.y = row * 64 + 63
        self.subject.add(puyo)
        return puyo

class TestBoard(TestBoardCommon):
    def setup(self):
        self.subject = Board(10, (15, 6), (64, 64))

    def test_initializing(self):
        assert_equal(self.subject.rows_count, 15)
        assert_equal(self.subject.cols_count, 6)
        assert_equal(self.subject.x, 10)
        assert_equal(self.subject.y, 74)
        assert_equal(self.subject.width, 64 * 6)
        assert_equal(self.subject.height, 64 * 14)
        assert_equal(self.subject.puyo_size, (64, 64))
        assert_equal(self.subject.current_pair, ())
        assert_equal(self.subject.state, 'placing')
        assert isinstance(self.subject.background, pygame.Surface)
        assert isinstance(self.subject.score, Score)

    def test_board(self):
        b = [[None, None, None, None, None, None] for row in range(15)]
        assert_equal(self.subject.board, b)
        self.subject.spawn_puyo_pair()
        b[0][2] = self.subject.sprites()[0]
        assert_equal(self.subject.board, b)

class TestBoardWithPuyoPair(TestBoardCommon):
    def setup(self):
        self.subject = Board(10, (15, 6), (64, 64))
        self.subject.spawn_puyo_pair()
        self.p1 = self.subject.sprites()[0]
        self.p2 = self.subject.sprites()[1]

    def test_spawning_puyos(self):
        assert_equal(len(self.subject), 2)
        assert isinstance(self.p1, Puyo)
        assert isinstance(self.p2, Puyo)
        assert_equal(self.p1.y, 0)
        assert_equal(self.p2.y, -64)

    def test_move_puyos_down(self):
        self.subject.update()
        assert_equal(self.p1.y, 1)
        assert_equal(self.p2.y, -63)

    def test_move_puyos_between_cells(self):
        self.p1.y = 63
        self.subject.update()
        assert_equal(self.subject.board[0][2], None)
        assert_equal(self.subject.board[1][2], self.p1)

    def test_not_move_puyos_each_on_another(self):
        self.p2.y = -1
        self.subject.update()
        assert_equal(self.p2.y, -1)

    def test_not_move_puyos_below_bottom(self):
        self.p1.y = self.subject.height - 1
        self.subject.update()
        assert_equal(self.p1.y, self.subject.height - 1)

    def test_rotate(self):
        self.subject.rotate()
        assert_equal(self.p2.row, 0)
        assert_equal(self.p2.col, 3)
        self.subject.rotate()
        assert_equal(self.p2.row, 1)
        assert_equal(self.p2.col, 2)
        self.subject.rotate()
        assert_equal(self.p2.row, 0)
        assert_equal(self.p2.col, 1)
        self.subject.rotate()
        assert_equal(self.p2.row, -1)
        assert_equal(self.p2.col, 2)

    def test_rotate_against_wall(self):
        self.p1.x = self.p2.x = 5 * 64
        self.subject.rotate()
        assert_equal(self.p2.col, 5)
        assert_equal(self.p1.col, 4)

        self.p1.x = self.p2.x = 0
        self.p2.y = 64
        self.subject.rotate()
        assert_equal(self.p2.col, 0)
        assert_equal(self.p1.col, 1)

    def test_rotate_against_wall_impossible(self):
        blocking_puyo = Puyo(self.subject, 'red')
        self.subject.add(blocking_puyo)
        blocking_puyo.x = 4 * 64
        self.p1.x = self.p2.x = 5 * 64
        self.subject.rotate()
        assert_equal(self.p2.row, -1)
        assert_equal(self.p1.col, 5)

        blocking_puyo.x = 64
        self.p1.x = self.p2.x = 0
        self.p2.y = 64
        self.subject.rotate()
        assert_equal(self.p2.row, 1)
        assert_equal(self.p1.col, 0)

    def test_rotate_without_current_pair(self):
        self.subject.current_pair = ()
        self.subject.rotate()

    def test_move_left(self):
        self.subject.move(False)
        assert_equal(self.p2.col, 1)
        assert_equal(self.p1.col, 1)

    def test_move_left_impossible(self):
        self.p2.x = 0
        self.p1.x = 64
        self.subject.move(False)
        assert_equal(self.p2.col, 0)
        assert_equal(self.p1.col, 1)

    def test_move_right(self):
        self.subject.move(True)
        assert_equal(self.p2.col, 3)
        assert_equal(self.p1.col, 3)

    def test_move_right_impossible(self):
        self.p2.x = 4 * 64
        self.p1.x = 5 * 64
        self.subject.move(True)
        assert_equal(self.p2.col, 4)
        assert_equal(self.p1.col, 5)

    def test_move_without_current_pair(self):
        self.subject.current_pair = ()
        self.subject.move(True)

    def test_reset_current_pair(self):
        self.subject.update()
        self.subject.update()
        assert_equal(self.subject.current_pair, (self.p1, self.p2))
        self.p2.y = self.subject.height - 1
        self.subject.update()
        assert_equal(self.subject.current_pair, ())
        assert_equal(self.subject.state, 'scoring')

    def test_reset_current_pair_if_dropped_on_other_puyo(self):
        self.p2.y = self.subject.height - 65
        self.add_puyo('red', 13, 2)
        self.subject.update()
        assert_equal(self.subject.current_pair, ())

    def test_fast_forward(self):
        puyo = self.add_puyo('red', 3, 3)
        self.subject.update(True)
        assert_equal(puyo.y, 4 * 64)
        assert_equal(self.p1.y, 15)
        assert_equal(self.p2.y, -49)

class TestBoardWithPuyos(TestBoardCommon):
    def setup(self):
        self.subject = Board(10, (15, 6), (64, 64))
        self.add_puyo('red', 14, 0)
        self.add_puyo('red', 14, 1)
        self.add_puyo('red', 13, 0)
        self.subject.state = 'scoring'

    def test_deletes_four_touching_puyos(self):
        self.add_puyo('red', 12, 0)
        self.subject.update()
        assert_equal(len(self.subject), 0)
        assert_equal(self.subject.board[12][0], None)
        assert_equal(self.subject.board[14][0], None)
        assert_equal(self.subject.board[14][1], None)
        assert_equal(self.subject.board[13][0], None)
        assert_equal(self.subject.state, 'scoring')

    def test_deletes_only_if_nothing_is_dropping(self):
        self.add_puyo('red', 12, 0)
        self.add_puyo('red', 1, 0)
        self.subject.update()
        assert_equal(len(self.subject), 5)
        assert_equal(self.subject.state, 'scoring')

    def test_does_not_delete_less_than_four(self):
        self.subject.update()
        assert_equal(len(self.subject), 5)

    def test_deletes_only_same_color(self):
        self.add_puyo('green', 12, 0)
        self.subject.update()
        assert_equal(len(self.subject), 6)

    def test_score_score(self):
        self.add_puyo('red', 12, 0)
        self.subject.update()
        assert_equal(self.subject.score.points, 40)

    def test_switched_back_to_placing_state(self):
        self.subject.score.chain = 1
        self.subject.update()
        assert_equal(self.subject.state, 'placing')
        assert_equal(len(self.subject), 5)
        assert_equal(self.subject.score.chain, 0)

