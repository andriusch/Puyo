import pygame, os

class Movable():
    def __init__(self, rect, parent = None):
        self.x = rect.left
        self.y = rect.top
        self.width = rect.width
        self.height = rect.height
        self.parent = parent
        
    def create_rect(self, x, y, width, height):
        if self.parent:
            x += self.parent.x
            y += self.parent.y
        return pygame.Rect(x, y, width, height)
        
    def get_rect(self):
        return self.create_rect(self.x, self.y, self.width, self.height)
    rect = property(get_rect)

class Sprite(pygame.sprite.Sprite):
    def load_image(self, path):
        fullname = os.path.join('data', path)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
        #self.image = self.image.convert()
        #self.image.set_colorkey(self.image.get_at((0,0)), pygame.RLEACCEL)
        return image
