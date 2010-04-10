import pygame, random
from puyo import *
COLORS = ['blue', 'green', 'purple', 'red', 'yellow']

class Board(pygame.sprite.Group, Movable):
    def __init__(self, puyo_size):
        pygame.sprite.Group.__init__(self)
        self.rows_count = 14
        self.cols_count = 6
        Movable.__init__(self, pygame.Rect(10, 10, puyo_size[0] * 6, puyo_size[1] * 14))
        
        background = pygame.sprite.Sprite()
        background.image = pygame.Surface(self.rect.size)
        background.image.fill((240, 240, 240))
        background.rect = self.rect
        self.add(background)
        
        self.puyo_size = puyo_size
        
    def spawn_puyo(self):
        self.add(Puyo(self, random.choice(COLORS)))
        self.add(Puyo(self, random.choice(COLORS), -1))
