import pygame,sys
from pygame.locals import *
from game import*
from const import * 
from blockGroup import *
from block import*
from utiles import *

pygame.init()
pygame.display.set_caption("Block Fall")
DISPALYSURF=pygame.display.set_mode((GAME_WIDTH_SIZE,GAME_HEIGHT_SIZE))
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