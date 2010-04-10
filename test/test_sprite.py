from puyo.sprite import *
from nose.tools import *
import pygame

class TestMovable:
    def setUp(self):
        self.subject = Movable(pygame.Rect(10, 20, 32, 64))
    
    def test_initializing(self):
        assert_equal(self.subject.x, 10)
        assert_equal(self.subject.y, 20)
        assert_equal(self.subject.width, 32)
        assert_equal(self.subject.height, 64)
        
    def test_rect(self):
        assert_equal(self.subject.create_rect(0, 1, 2, 3), pygame.Rect(0, 1, 2, 3))
        assert_equal(self.subject.rect, pygame.Rect(10, 20, 32, 64))
        
    def test_rect_with_parent(self):
        rect = Movable(pygame.Rect(5, 6, 7, 8), self.subject)
        assert_equal(rect.create_rect(0, 1, 2, 3), pygame.Rect(10, 21, 2, 3))
        assert_equal(rect.rect, pygame.Rect(15, 26, 7, 8))