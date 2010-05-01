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

board = Board((32, 32))
board.spawn_puyo_pair()
clock = pygame.time.Clock()

while 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                board.rotate()
            if event.key == K_LEFT:
                board.move_left()
            if event.key == K_RIGHT:
                board.move_right()

    board.update()

    screen.blit(background, (0, 0))
    board.draw(screen)
    pygame.display.flip()

