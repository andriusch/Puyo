import pygame, random
from puyo import *
from score import *

class Board(pygame.sprite.Group, Movable):
    def __init__(self, x, size, puyo_size):
        pygame.sprite.Group.__init__(self)
        self.rows_count = size[0]
        self.cols_count = size[1]
        Movable.__init__(self, pygame.Rect(x, 10 + puyo_size[1], puyo_size[0] * self.cols_count, puyo_size[1] * self.rows_count))

        self.background = pygame.Surface(self.rect.size)
        self.background.fill((240, 240, 240))

        self.puyo_size = puyo_size
        self._board = None
        self.current_pair = ()
        self.state = 'placing'
        self.score = Score(self, pygame.Rect(0, -puyo_size[1], self.width, puyo_size[1]))
        self.game_over = False

    def spawn_puyo_pair(self):
        self.current_pair = (self.__spawn_puyo(0), self.__spawn_puyo(1))
        self.score.generate_next_pair()
        self._board = None
        self.score.chain = 0
        self.spawned = True

    def move(self, right):
        if not self.current_pair:
            return
        first, second = sorted(self.current_pair, key=lambda puyo: puyo.x, reverse=right)
        dx = self.puyo_size[0] if right else -self.puyo_size[0]
        if self.__move_puyo(first, dx, 0):
            self.__move_puyo(second, dx, 0)

    def rotate(self):
        if not self.current_pair:
            return

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

    def __spawn_puyo(self, index):
        puyo = Puyo(self, self.score.next_pair[index].color, index - 1)
        if puyo.row >= 0 and not (self.board[puyo.row][puyo.col] is None):
            self.game_over = True
        self.add(puyo)
        return puyo

    def __spawn_neutrals(self):
        column_drops, left_drops = divmod(self.score.drop_neutrals, self.cols_count)
        neutral_counts = [column_drops] * self.cols_count
        for ind in range(left_drops):
            neutral_counts[ind] += 1
        random.shuffle(neutral_counts)
        for col, neutral_count in enumerate(neutral_counts):
            for row in range(neutral_count):
                puyo = NeutralPuyo(self, 0 - row, col)
                self.add(puyo)
        self.score.drop_neutrals = 0

    def update(self, fast_forward = False):
        self.spawned = False
        pygame.sprite.Group.update(self)
        self.__reset_current_pair(fast_forward)

        dropping = False
        for puyo in sorted(self, key=lambda puyo: puyo.row, reverse=True):
            speed = puyo.speed(fast_forward and puyo in self.current_pair)
            if self.__move_puyo(puyo, 0, speed):
                dropping = True

        if self.state == 'scoring' and not dropping:
            if not self.__scan_puyo_combos():
                if self.score.drop_neutrals:
                    self.__spawn_neutrals()
                else:
                    self.state = 'placing'
                    self.spawn_puyo_pair()
        self._board = None

    def __reset_current_pair(self, fast_forward):
        for puyo in self.current_pair:
            if not self.__can_move(puyo, 0, puyo.speed(fast_forward), self.current_pair):
                self.current_pair = ()
                self.state = 'scoring'
                return

    def __scan_puyo_combos(self):
        for puyo in self:
            result = set([])
            self.__scan_puyo_combos_from(puyo, puyo, result)

            if self.score.add_score(result):
                self.remove(*result)
                for deleted_puyo in result:
                    self.board[deleted_puyo.row][deleted_puyo.col] = None

        return self.score.scored()

    def __scan_puyo_combos_from(self, puyo, last_puyo, result):
        if puyo is None or puyo in result or not last_puyo.same_color(puyo):
            return
        result.add(puyo)
        if puyo.row < self.rows_count - 1:
            self.__scan_puyo_combos_from(self.board[puyo.row + 1][puyo.col], puyo, result)
        if puyo.row > 0:
            self.__scan_puyo_combos_from(self.board[puyo.row - 1][puyo.col], puyo, result)
        if puyo.col < self.cols_count - 1:
            self.__scan_puyo_combos_from(self.board[puyo.row][puyo.col + 1], puyo, result)
        if puyo.col > 0:
            self.__scan_puyo_combos_from(self.board[puyo.row][puyo.col - 1], puyo, result)


    def draw(self, surface):
        surface.blit(self.background, self.rect)
        for puyo in self:
            if puyo.row >= 0:
                surface.blit(puyo.image, puyo.rect)
        surface.blit(self.score.image, self.score.rect)

    def __move_puyo(self, puyo, dx, dy):
        if puyo:
            if self.__can_move(puyo, dx, dy):
                puyo.y += dy
                puyo.x += dx
                return True
        else:
                return False

    def __can_move(self, puyo, dx, dy, non_blocking_puyos = ()):
        x = puyo.x + dx
        y = puyo.y + dy
        col = puyo.get_col(x)
        row = puyo.get_row(y)
        if puyo.row == row and puyo.col == col:
            return True
        elif y >= self.height or x < 0 or x >= self.width:
            return False
        else:
            blocking_puyo = None
            for puyo in self:
                if puyo.row == row and puyo.col == col:
                    blocking_puyo = puyo
            return blocking_puyo is None or (blocking_puyo in non_blocking_puyos)

    def empty_board(self):
        return [[None for col in range(self.cols_count)] for row in range(self.rows_count)]

    def get_board(self):
        if self._board is None:
            self._board = self.empty_board()
            for puyo in self:
                if puyo.row >= 0:
                    self._board[puyo.row][puyo.col] = puyo
        return self._board
    board = property(get_board)

