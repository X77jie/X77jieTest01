from typing import Any
import pygame,sys
from pygame.locals import *
from blockGroup import *
from const import *

class Game(pygame.sprite.Sprite):
    def __init__(self,surface):
        self.surface=surface
        self.fixedBlockGroup=BlockGroup(BlockGroupType.FIXED,BLOCK_SIZE_W,BLOCK_SIZE_H,[],self.getRelPos())
        self.dropBlockGroup=None
        self.gameOverImage=pygame.image.load('game over.png')
        self.isGameOver=False

    def generateDropBlockGroup(self):
        conf=BlockGroup.GenerateBlockGroupConfig(0,GAME_COL/2-1)
        self.dropBlockGroup=BlockGroup(BlockGroup.DROP,BLOCK_SIZE_W,BLOCK_SIZE_H,conf,self.getRelPos())

    
    def draw(self):
        self.fixedBlockGroup.draw(self.surface)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.surface)
        #     self.dropBlockGrop.update()
        if self.isGameOver:
            rect= self.gameOverImage.get_rect()
            rect.center=GAME_WIDTH_SIZE /2
            rect.center=GAME_HEIGHT_SIZE /2
            self.surface.blit(self.gameOverImage,rect)
        else:
            self.generateDropBlockGroup()#方法调用加上()
    
    def getRelPos(self): 
        return(240,50)
    
    def willcollide(self):
        hash={}
        allIndex=self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndex:
            hash[idx]=1
        dropIndexes=self.dropBlockGroup.getNextBlockIndexes()

        for dropIdex in dropIndexes:
            if hash.get(dropIdex):
                return True
            if dropIdex[0]>=GAME_ROW:
                return True
            return False

    def update(self):#12：59时可以修改
        if self.isGameOver:

            return

        self.checkGameOver()

        # self.fixedBlockGroup.update()#ai修改
        # # 初始化self.fixedBlockGroup
        # self.fixedBlockGroup = FixedBlockGroup()#ai修改
        # 调用self.fixedBlockGroup的update方法
        self.fixedBlockGroup.update()

        if self.fixedBlockGroup.IsEliminating():
            return
        if self.dropBlockGroup:
            self.dropBlockGroup.update()
        else:
            self.generateDropBlockGroup()

        if self.willcollide():
            blocks=self.dropBlockGroup.getBlocks()
            for blk in blocks:
                self.fixedBlockGroup.addBlock(blk)
            self.dropBlockGroup.clearBlocks()
            self.dropBlockGroup=None
            self.fixedBlockGroup.processEliminate()

    def checkGameOver(self):
        allIndexes=self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            if idx[0]<2:
                self.isGameOver=True





    