from puyo.board import *
from nose.tools import *
import pygame

class TestMovable:
    def setUp(self):
        self.subject = Board((64, 64))

    def test_initializing(self):
        assert_equal(self.subject.rows_count, 14)
        assert_equal(self.subject.cols_count, 6)
        assert_equal(self.subject.x, 10)
        assert_equal(self.subject.y, 10)
        assert_equal(self.subject.width, 64 * 6)
        assert_equal(self.subject.height, 64 * 14)
        assert_equal(self.subject.puyo_size, (64, 64))
        
    def test_initialized_with_background(self):
        print self.subject.sprites()
        bg = self.subject.sprites()[0]
        assert isinstance(bg, pygame.sprite.Sprite)
        print bg, bg.rect, self.subject.rect
        assert_equal(bg.rect, self.subject.rect)