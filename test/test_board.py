from puyo.board import *
from nose.tools import *
import pygame

class TestBoard:
    def setup(self):
        self.subject = Board((64, 64))

    def test_initializing(self):
        assert_equal(self.subject.rows_count, 15)
        assert_equal(self.subject.cols_count, 6)
        assert_equal(self.subject.x, 10)
        assert_equal(self.subject.y, 10)
        assert_equal(self.subject.width, 64 * 6)
        assert_equal(self.subject.height, 64 * 14)
        assert_equal(self.subject.puyo_size, (64, 64))

    def test_initialized_with_background(self):
        assert isinstance(self.subject.background, pygame.Surface)

    def test_board(self):
        b = [[None, None, None, None, None, None] for row in range(15)]
        assert_equal(self.subject.board, b)
        self.subject.spawn_puyo_pair()
        b[0][2] = self.subject.sprites()[0]
        assert_equal(self.subject.board, b)

class TestBoardWithPuyos:
    def setup(self):
        self.subject = Board((64, 64))
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

