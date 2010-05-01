import pygame
from sprite import *

class Puyo(Sprite, Movable):
    def __init__(self, parent, color, row = 0):
        Sprite.__init__(self) #call Sprite initializer
        self.image = pygame.transform.smoothscale(Sprite.load_image(self, 'puyo_%s.png' % color), parent.puyo_size)
        width, height = parent.puyo_size
        Movable.__init__(self, pygame.Rect(2 * width, row * height, width, height), parent)

    def get_row(self, y = None):
        if y is None:
            y = self.y
        return y / self.height
    row = property(get_row)

    def get_col(self, x = None):
        if x is None:
            x = self.x
        return x / self.width
    col = property(get_col)

    def get_rect(self):
        return self.create_rect(self.col * self.width, self.row * self.height, self.width, self.height)
    rect = property(get_rect)

