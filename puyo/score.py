import pygame
from puyo import *

class Score(object):
    def __init__(self, rect):
        self.rect = rect
        self._font = pygame.font.SysFont(None, rect.height / 2)
        self.image = pygame.Surface(rect.size)
        self._last_scored = 0
        self._last_multi = 0
        self.chain = 0
        self.points = 0
        self.drop_neutrals = 0
        self._neutrals_scored = 0

    def get_points(self):
        return self._points

    def set_points(self, value):
        self.image.fill((255, 180, 30))
        score_image = self._font.render(str(value), True, (0, 0, 0))
        self.image.blit(score_image, (4, 4))

        if self._last_scored > 0:
            last_score = "%dx%d" % (self._last_scored, self._last_multi)
            last_score_image = self._font.render(last_score, True, (0, 0, 0))
            self.image.blit(last_score_image, (4, self.rect.height / 2 + 4))

        self._points = value

    points = property(get_points, set_points)

    def add_score(self, puyos):
        normal_puyos = [puyo for puyo in puyos if not isinstance(puyo, NeutralPuyo)]
        if len(normal_puyos) >= 4:
            self._last_scored += len(normal_puyos) * 10
            multi = len(normal_puyos) - 4 + self.chain * 8
            self._last_multi += (multi or 1)
            return True
        else:
            return False

    def scored(self):
        if self._last_scored > 0:
            self.chain += 1
            points = self._last_scored * self._last_multi
            self.points += points
            self._neutrals_scored = points / 50
            result = True
        else:
            result = False

        self._last_scored = 0
        self._last_multi = 0
        return result

    def neutrals_scored(self):
        scored = self._neutrals_scored
        self._neutrals_scored = 0
        return scored

