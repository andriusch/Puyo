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
        self.current_pair = (self.__spawn_puyo(self.rows_count - 2), self.__spawn_puyo(self.rows_count - 1))
        self._board = None

    def move_left(self):
        left, right = sorted(self.current_pair, key=lambda puyo: puyo.x)
        if self.__move_puyo(left, -self.puyo_size[0], 0):
            self.__move_puyo(right, -self.puyo_size[0], 0)

    def move_right(self):
        left, right = sorted(self.current_pair, key=lambda puyo: puyo.x)
        if self.__move_puyo(right, self.puyo_size[0], 0):
            self.__move_puyo(left, self.puyo_size[0], 0)

    def rotate(self):
        if self.current_pair[0].row == self.current_pair[1].row:
            if self.current_pair[0].col > self.current_pair[1].col:
                self.__move_puyo(self.current_pair[1], self.puyo_size[0], -self.puyo_size[1])
            else:
                self.__move_puyo(self.current_pair[1], -self.puyo_size[0], self.puyo_size[1])
        else:
            if self.current_pair[0].row > self.current_pair[1].row:
                # Prie desines sienos
                if self.current_pair[1].col == self.cols_count - 1:
                    if self.__move_puyo(self.current_pair[0], -self.puyo_size[0], 0):
                        self.__move_puyo(self.current_pair[1], 0, self.puyo_size[1])
                else:
                    self.__move_puyo(self.current_pair[1], self.puyo_size[0], self.puyo_size[1])
            else:
                # Prie kaires sienos
                if self.current_pair[1].col == 0:
                    if self.__move_puyo(self.current_pair[0], self.puyo_size[0], 0):
                        self.__move_puyo(self.current_pair[1], 0, -self.puyo_size[1])
                else:
                    self.__move_puyo(self.current_pair[1], -self.puyo_size[0], -self.puyo_size[1])
        self._board = None

    def __spawn_puyo(self, row):
        puyo = Puyo(self, random.choice(COLORS), self.rows_count - row - 2)
        self.add(puyo)
        return puyo

    def update(self, *args):
        pygame.sprite.Group.update(self, *args)
        for puyo in sorted(self, key=lambda puyo: puyo.row, reverse=True):
            self.__move_puyo(puyo, 0, 1)
        self._board = None

    def draw(self, surface):
        surface.blit(self.background, self.rect)
        for puyo in self:
            if puyo.row >= 0:
                surface.blit(puyo.image, puyo.rect)

    def __move_puyo(self, puyo, dx, dy):
        if puyo:
            if self.__can_move(puyo, puyo.x + dx, puyo.y + dy):
                puyo.y += dy
                puyo.x += dx
                return True
        else:
                return False

    def __can_move(self, puyo, x, y):
        row = puyo.get_row(y)
        col = puyo.get_col(x)
        if puyo.row == row and puyo.col == col:
            return True
        elif y >= self.height or x < 0 or x >= self.width:
            return False
        else:
            blocking_puyo = self.board[row][col]
            if blocking_puyo and blocking_puyo.row == row and blocking_puyo.col == col:
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

