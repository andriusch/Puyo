import pygame
from sprite import *

class Puyo(Sprite, Movable):
    def __init__(self, parent, color, row = 0, col = 2):
        Sprite.__init__(self) #call Sprite initializer
        self.image = pygame.transform.smoothscale(Sprite.load_image(self, 'puyo_%s.png' % color), parent.puyo_size)
        width, height = parent.puyo_size
        Movable.__init__(self, pygame.Rect(col * width, row * height, width, height), parent)
        self.color = color
        self.speed = 1
        self.points = 10

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

    def same_color(self, other_puyo):
        return self.color == other_puyo.color or other_puyo.color == 'neutral'

class NeutralPuyo(Puyo):
    def __init__(self, parent, row, col):
        Puyo.__init__(self, parent, 'neutral', row, col)
        self.speed = 15
        self.points = 20

    def same_color(self, other_puyo):
        return False

