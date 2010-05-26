import pygame, random
from puyo import *
COLORS = ['blue', 'green', 'purple', 'red', 'yellow']

class Score(Movable):
    def __init__(self, parent, rect):
        Movable.__init__(self, rect, parent)
        self._font = pygame.font.SysFont(None, rect.height / 2)
        self.image = pygame.Surface(rect.size)

        self._last_scored = 0
        self._last_multi = 0
        self.chain = 0
        self._points = 0
        self.drop_neutrals = 0
        self._neutrals_scored = 0

        psize = self.height / 3
        self.next_pair_parent = Movable(pygame.Rect(self.width - psize * 3.5, psize * 1.5, psize, psize), self)
        self.next_pair_parent.puyo_size = (psize, psize)
        self.generate_next_pair()

    def generate_next_pair(self):
        puyo1 = Puyo(self.next_pair_parent, random.choice(COLORS), -1)
        puyo2 = Puyo(self.next_pair_parent, random.choice(COLORS), 0)
        self.next_pair = (puyo1, puyo2)
        self._generate_image()


    def get_points(self):
        return self._points

    def set_points(self, value):
        self._points = value
        self._generate_image()

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

    def _generate_image(self):
        self.image.fill((255, 180, 30))
        score_image = self._font.render(str(self.points), True, (0, 0, 0))
        self.image.blit(score_image, (4, 4))

        if self._last_scored > 0:
            last_score = "%dx%d" % (self._last_scored, self._last_multi)
            last_score_image = self._font.render(last_score, True, (0, 0, 0))
            self.image.blit(last_score_image, (4, self.height / 2 + 4))

        next_image = self._font.render("Next:", True, (0, 0, 0))
        self.image.blit(next_image, (self.width - self.height * 1.5,self.height / 2.5))
        for puyo in self.next_pair:
            self.image.blit(puyo.image, puyo.rect)

