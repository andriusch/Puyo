from puyo.score import *
from nose.tools import *
import pygame

class TestScore:
    def setup(self):
        pygame.init()
        self.subject = Score(pygame.Rect(0, 0, 128, 32))
        self.subject.puyo_size = (32, 32)

    def puyos(self, count, color = 'red'):
        return [Puyo(self.subject, color) for i in range(count)]
    def neutral_puyos(self, count):
        return [NeutralPuyo(self.subject, 0, 0) for i in range(count)]

    def test_initializing(self):
        assert_equal(self.subject.points, 0)
        assert_equal(self.subject.rect, pygame.Rect(0, 0, 128, 32))

    def test_no_score(self):
        assert_equal(self.subject.scored(), False)

    def test_does_not_count_less_than_four(self):
        assert_false(self.subject.add_score(self.puyos(3)))
        assert_false(self.subject.scored())

    def test_does_not_count_neutrals_into_four_required(self):
        assert_false(self.subject.add_score(self.puyos(3) + self.neutral_puyos(2)))

    def test_score_4(self):
        assert self.subject.add_score(self.puyos(4))
        assert self.subject.scored()
        assert_equal(self.subject.points, 40)

    def test_calculates_chain(self):
        self.subject.chain = 1
        self.subject.add_score(self.puyos(4))
        self.subject.scored()
        assert_equal(self.subject.chain, 2)

    def test_score_5(self):
        self.subject.add_score(self.puyos(5))
        self.subject.scored()
        assert_equal(self.subject.points, 50)

    def test_score_6(self):
        self.subject.add_score(self.puyos(6))
        self.subject.scored()
        assert_equal(self.subject.points, 120)

    def test_score_4_4(self):
        self.subject.add_score(self.puyos(4))
        self.subject.add_score(self.puyos(4))
        self.subject.scored()
        assert_equal(self.subject.points, 160)

    def test_score_4_chain_4(self):
        self.subject.add_score(self.puyos(4))
        self.subject.scored()
        self.subject.add_score(self.puyos(4))
        self.subject.scored()
        assert_equal(self.subject.points, 360)

    def test_score_with_neutrals(self):
        self.subject.add_score(self.puyos(4) + self.neutral_puyos(3))
        self.subject.scored()
        assert_equal(self.subject.points, 40)

    def test_calculated_count_of_puyos_to_drop(self):
        self.subject.add_score(self.puyos(6))
        self.subject.scored()
        assert_equal(self.subject.neutrals_scored(), 2)
        self.subject.add_score(self.puyos(4))
        self.subject.scored()
        assert_equal(self.subject.neutrals_scored(), 6)

