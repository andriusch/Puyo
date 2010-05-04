from puyo.board import *
from puyo.puyo import *
from nose.tools import *
import pygame

class TestPuyo:
    def setUp(self):
        self.board = Board((32, 32))
        self.puyo = Puyo(self.board, 'red')
        self.board.add(self.puyo)

    def test_initializing(self):
        assert isinstance(self.puyo.image, pygame.Surface)
        assert_equal(self.puyo.y, 0)
        assert_equal(self.puyo.x, 64)
        assert_equal(self.puyo.image.get_width(), 32)
        assert_equal(self.puyo.image.get_height(), 32)

    def test_return_correct_row(self):
        self.puyo.y = 63
        assert_equal(self.puyo.row, 1)
        self.puyo.y = 64
        assert_equal(self.puyo.row, 2)
        assert_equal(self.puyo.get_row(128), 4)

    def test_return_correct_col(self):
        self.puyo.x = 63
        assert_equal(self.puyo.col, 1)
        self.puyo.x = 64
        assert_equal(self.puyo.col, 2)
        assert_equal(self.puyo.get_col(128), 4)

    def test_updates_rectangle_on_move(self):
        self.puyo.y, self.puyo.x = 127, 127
        assert_equal(self.puyo.rect.top, 138)
        assert_equal(self.puyo.rect.left, 106)

        self.puyo.y, self.puyo.x = 128, 128
        assert_equal(self.puyo.rect.top, 170)
        assert_equal(self.puyo.rect.left, 138)

    def test_allows_passing_row_on_initialize(self):
        self.puyo = Puyo(self.board, 'red', -1)
        assert_equal(self.puyo.row, -1)

    def test_does_not_move_below_bottom(self):
        self.puyo.y = 13 * 32
        self.puyo.update()
        assert_equal(self.puyo.y, 13 * 32)

    def test_same_color(self):
        assert self.puyo.same_color(Puyo(self.board, 'red'))
        assert_false(self.puyo.same_color(Puyo(self.board, 'green')))

