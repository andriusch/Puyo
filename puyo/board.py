import pygame, random
from puyo import *
COLORS = ['blue', 'green', 'purple', 'red', 'yellow']

class Board(pygame.sprite.Group, Movable):
    def __init__(self, puyo_size):
        pygame.sprite.Group.__init__(self)
        self.rows_count = 15
        self.cols_count = 6
        Movable.__init__(self, pygame.Rect(10, 10, puyo_size[0] * self.cols_count, puyo_size[1] * (self.rows_count - 1)))

        self.background = pygame.Surface(self.rect.size)
        self.background.fill((240, 240, 240))

        self.puyo_size = puyo_size
        self._board = None

    def spawn_puyo_pair(self):
        self.__spawn_puyo(self.rows_count - 2)
        self.__spawn_puyo(self.rows_count - 1)
        self._board = None

    def __spawn_puyo(self, row):
        puyo = Puyo(self, random.choice(COLORS), self.rows_count - row - 2)
        self.add(puyo)

    def update(self, *args):
        pygame.sprite.Group.update(self, *args)
        for puyo in self:
            self.__move_puyo(puyo, 0, 1)
        self._board = None

    def draw(self, surface):
        surface.blit(self.background, self.rect)
        pygame.sprite.Group.draw(self, surface)

    def __move_puyo(self, puyo, dx, dy):
        if puyo:
            new_row = puyo.get_row(puyo.y + dy)
            if self.is_free(puyo, new_row):
                puyo.y += dy

    def is_free(self, puyo, row):
        if puyo.row == row:
            return True
        elif puyo.y >= self.height - 1:
            return False
        else:
            blocking_puyo = self.board[row][puyo.col]
            if blocking_puyo and blocking_puyo.row == row:
                return False
            else:
                return True

    def get_board(self):
        if self._board is None:
            self._board = [[None for col in range(self.cols_count)] for row in range(self.rows_count)]
            for puyo in self:
                if puyo.row >= 0:
                    self._board[puyo.row][puyo.col] = puyo
        return self._board
    board = property(get_board)

