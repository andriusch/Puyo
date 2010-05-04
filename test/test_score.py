from puyo.score import *
from nose.tools import *
import pygame

class TestScore:
    def setup(self):
        pygame.init()
        self.subject = Score(pygame.Rect(0, 0, 128, 32))

    def test_initializing(self):
        assert_equal(self.subject.points, 0)
        assert_equal(self.subject.rect, pygame.Rect(0, 0, 128, 32))

    def test_no_score(self):
        assert_equal(self.subject.scored(), False)

    def test_score_4(self):
        self.subject.add_score(4)
        assert self.subject.scored()
        assert_equal(self.subject.points, 40)

    def test_calculates_chain(self):
        self.subject.chain = 1
        self.subject.add_score(4)
        self.subject.scored()
        assert_equal(self.subject.chain, 2)

    def test_score_5(self):
        self.subject.add_score(5)
        self.subject.scored()
        assert_equal(self.subject.points, 50)

    def test_score_6(self):
        self.subject.add_score(6)
        self.subject.scored()
        assert_equal(self.subject.points, 120)

    def test_score_4_4(self):
        self.subject.add_score(4)
        self.subject.add_score(4)
        self.subject.scored()
        assert_equal(self.subject.points, 160)

    def test_score_4_chain_4(self):
        self.subject.add_score(4)
        self.subject.scored()
        self.subject.add_score(4)
        self.subject.scored()
        assert_equal(self.subject.points, 360)

