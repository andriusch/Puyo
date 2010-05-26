#!/usr/bin/env python

import sys
import pygame
from pygame.locals import *

from board import *
from player import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Puyo Pop')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
screen.blit(background, (0, 0))
pygame.display.flip()

puyo_size = (48, 48)
board_size = (11, 6)
player1 = HumanPlayer(Board(10, board_size, puyo_size), (K_UP, K_LEFT, K_RIGHT, K_DOWN))
player2 = ComputerPlayer(Board(410, board_size, puyo_size))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 150)
pause = False

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_p:
                pause = not pause
            player1.key_press(event.key)
            player2.key_press(event.key)

    if player1.game_over() or player2.game_over():
        text = "Player 2 won!" if player1.game_over() else "Player 1 won!"
        screen.blit(background, (0, 0))
        screen.blit(font.render(text, True, (0, 255, 0)), (50, 250))
    else:
        if not pause:
            player1.update()
            player2.update()
            player1.drop_neutrals(player2)
            player2.drop_neutrals(player1)

        screen.blit(background, (0, 0))
        player1.board.draw(screen)
        player2.board.draw(screen)

    pygame.display.flip()

