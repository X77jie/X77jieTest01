import random
import time
import pygame
import sys
from pygame.locals import *
from block import Block
from const import *
pygame.init()
DISPALYSURF=pygame.display.set_mode((GAME_WIDTH_SIZE,GAME_HIGHT_SIZE))
game=Game(DISPALYSURF)


while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        game.update()
        DISPALYSURF.fill((0,0,0))#(0,0,0)代表黑色的RGB值
        game.draw()
        pygame.display.update()