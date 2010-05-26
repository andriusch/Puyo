import pygame

class Player(object):
    def __init__(self, board):
        self.board = board
        board.spawn_puyo_pair()

    def update(self, fast):
        self.board.update(fast)

    def drop_neutrals(self, other):
        self.board.score.drop_neutrals += other.board.score.neutrals_scored()

    def game_over(self):
        return self.board.game_over


class HumanPlayer(Player):
    def __init__(self, board, keys):
        Player.__init__(self, board)
        self.rotate_key, self.left_key, self.right_key, self.speed_key = keys

    def key_press(self, key):
        if key == self.rotate_key:
            self.board.rotate()
        elif key == self.left_key:
            self.board.move(False)
        elif key == self.right_key:
            self.board.move(True)

    def update(self):
        Player.update(self, pygame.key.get_pressed()[self.speed_key])

class ComputerPlayer(Player):
    def key_press(self, key):
        pass

    def update(self):
        Player.update(self, False)

