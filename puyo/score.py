import pygame

class Score(object):
    def __init__(self, rect):
        self.rect = rect
        self._font = pygame.font.SysFont(None, rect.height / 2)
        self.image = pygame.Surface(rect.size)
        self._last_scored = 0
        self._last_multi = 0
        self.chain = 0
        self.points = 0

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
        self._last_scored += puyos * 10
        multi = puyos - 4 + self.chain * 8
        self._last_multi += (multi or 1)

    def scored(self):
        if self._last_scored > 0:
            self.chain += 1
            self.points += self._last_scored * self._last_multi
            result = True
        else:
            result = False

        self._last_scored = 0
        self._last_multi = 0
        return result

