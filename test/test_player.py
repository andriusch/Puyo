from puyo.player import *
from puyo.board import *
from nose.tools import *
import pygame
pygame.init()

class TestAI():
    def add_puyo(self, color, row, col):
        self.board.add(Puyo(self.board, color, row, col))

    def set_next_pair(self, color1, color2):
        self.board.score.next_pair[0].color = color1
        self.board.score.next_pair[1].color = color2

    def setup(self):
        self.board = Board(10, (10, 5), (32, 32))
        self.add_puyo('yellow', 7, 0)
        self.add_puyo('yellow', 8, 0)
        self.add_puyo('yellow', 9, 0)

    def test_ai_move(self):
        self.set_next_pair('yellow', 'green')
        player = ComputerPlayer(self.board)
        self.set_next_pair('yellow', 'yellow')
        player.next_move()
        assert_equal(player.move, [2, 0, 19])

    def test_ai_tries_to_minimize_height(self):
        self.set_next_pair('green', 'red')
        player = ComputerPlayer(self.board)
        self.set_next_pair('green', 'red')
        player.next_move()
        assert_equal(player.move, [1, 0, -1])

