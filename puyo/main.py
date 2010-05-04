#!/usr/bin/env python

import sys
import pygame
from pygame.locals import *

from board import *

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
board_size = (12, 6)
board = Board(410, board_size, puyo_size)
board.spawn_puyo_pair()
board2 = Board(10, board_size, puyo_size)
board2.spawn_puyo_pair()
clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                board.rotate()
            if event.key == K_LEFT:
                board.move(False)
            if event.key == K_RIGHT:
                board.move(True)
            if event.key == K_w:
                board2.rotate()
            if event.key == K_a:
                board2.move(False)
            if event.key == K_d:
                board2.move(True)

    board.update(pygame.key.get_pressed()[K_DOWN])
    board2.update(pygame.key.get_pressed()[K_s])

    screen.blit(background, (0, 0))
    board.draw(screen)
    board2.draw(screen)
    pygame.display.flip()

