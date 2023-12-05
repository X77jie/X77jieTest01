import random
import time
import pygame
import sys
from pygame.locals import *
from block import Block
from const import *
from game import*

def getCurrentTime():
    t = time.time()
    return int(t * 100)

class BlockType:
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    PURPLE = 4
    BLUE = 5

class BlockGroupType:
    FIXED = 0
    DROP = 1

BLOCK_RES = {
    BlockType.RED: "red.png",
    BlockType.ORANGE: "orange.png",
    BlockType.YELLOW: "yellow.png",
    BlockType.GREEN: "green.png",
    BlockType.PURPLE: "purple.png",
    BlockType.BLUE: "blue.png",
}

GAME_ROW = 17
GAME_COL = 10

BLOCK_SIZE_W = 32
BLOCK_SIZE_H = 32

GAME_WIDTH_SIZE = 800
GAME_HEIGHT_SIZE = 600

BLOCK_SHAPE = [
    [(0,0),(0,1),(1,0),(1,1)],  # 方形
    [(0,0),(0,1),(0,2),(0,3)],  # 长条
    [(0,0),(0,1),(1,1),(1,2)],  # z字形
    [(0,1),(1,0),(1,1),(1,2)],  # 飞机形
]

BLOCK_SHAPE = [
    [((0,0),(0,1),(1,0),(1,1)),],
    [((0,0),(0,1),(0,2),(0,3)),((0,0),(1,0),(2,0),(3,0))],
    [((0,0),(0,1),(1,1),(1,2)),((0,1),(1,0),(1,1),(2,0))],
    [((0,1),(1,0),(1,1),(1,2)),((0,1),(1,1),(1,2),(2,1)),((1,0),(1,1),(1,2),(2,1),(0,1),(1,0),(1,1),(2,1))],
]

class BlockGroup(object):
    def __init__(self, blockGroupType, width, height, blockConfigList, relPos):
        self.blocks = []
        self.time = 0
        self.pressTime = {}
        self.blockGroupType = blockGroupType
        self.isEliminating = False
        self.dropInterval = 300
        for config in blockConfigList:
            blk = Block(config["blockType"], config['rowIdx'], config['colIdx'], width, height, relPos)
            self.blocks.append(blk)

    def draw(self, surface):
        for blk in self.blocks:
            blk.draw(surface)

    def update(self):
        oldTime = self.time
        curTime = getCurrentTime()
        diffTime = curTime - oldTime
        if self.blockGroupType == BlockGroupType.DROP:
            if diffTime >= self.dropInterval:
                self.time = curTime
                for blk in self.blocks:
                    blk.drop()
            self.keyDownHandler()

        for blk in self.blocks:
            blk.update()

        if self.IsEliminating():
            if getCurrentTime() - self.eliminateTime > 500:
                tempBlocks = []
                for blk in self.blocks:
                    if blk.getIndex()[0] != self.eliminateRow:
                        if blk.getIndex()[0] < self.eliminateRow:
                            blk.drop()
                        tempBlocks.append(blk)
                self.blocks = tempBlocks
                self.setEliminate(False)

    def getBlockIndexes(self):
        return [block.getIndex() for block in self.blocks]

    def getNextBlockIndexes(self):
        return [block.getNextIndex() for block in self.blocks]

    def getBlocks(self):
        return self.blocks

    def isLeftBound(self):
        return self.colIdx == 0

    def isRightBound(self):
        return self.colIdx == GAME_COL - 1

    def doLeft(self):
        self.colIdx -= 1

    def doRight(self):
        self.colIdx += 1

    def clearBlocks(self):
        self.blocks = []

    def addBlock(self, blk):
        self.blocks.append(blk)

    def checkAndSetPressTime(self, key):
        ret = False
        if getCurrentTime() - self.pressTime.get(key, 0) > 30:
            ret = True
            self.pressTime[key] = getCurrentTime()
            return ret

    def keyDownHandler(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and self.checkAndSetPressTime(K_LEFT):
            b = True
            for blk in self.blocks:
                if blk.isLeftBound():
                    b = False
                    break
            if b:
                for blk in self.blocks:
                    blk.doLeft()
        elif pressed[K_RIGHT] and self.checkAndSetPressTime(K_RIGHT):
            b = True
            for blk in self.blocks:
                if blk.isRightBound():
                    b = False
                    break
            if b:
                for blk in self.blocks:
                    blk.doRight()
        if pressed[K_DOWN]:
            self.dropInterval = 30
        else:
            self.dropInterval = 800
        if pressed[K_UP] and self.checkAndSetPressTime(K_UP):
            for blk in self.blocks:
                blk.doRotate()

    def doEliminate(self, row):
        eliminateRow = {}
        for col in range(0, GAME_COL):
            idx = (row, col)
            eliminateRow[idx] = 1
        for blk in self.blocks:
            if eliminateRow.get(blk.getIndex()):
                blk.startBlink()

    def processEliminate(self):
        hash = {}
        allIndexes = self.getBlockIndexes()
        for idx in allIndexes:
            for idx in allIndexes:
                hash[idx] = 1
        for row in range(GAME_ROW - 1, -1, -1):
            full = True
            for col in range(0, GAME_COL):
                idx = (row, col)
                if not hash.get(idx):
                    full = False
                    break
            if full:
                self.doEliminate(row)
                return

    def setEliminate(self, e1):
        self.isEliminating = e1

    def IsEliminating(self):
        return self.isEliminating

class Game(pygame.sprite.Sprite):
    def __init__(self, surface):
        self.surface = surface
        self.fixedBlockGroup = BlockGroup(BlockGroupType.FIXED, BLOCK_SIZE_W, BLOCK_SIZE_H, [], self.getRelPos())
        self.dropBlockGroup = None
        self.gameOverImage = pygame.image.load('gameover.bmp')
        self.isGameOver = False

    def generateDropBlockGroup(self):
        conf = BlockGroup.GenerateBlockGroupConfig(0, GAME_COL // 2 - 1)
        self.dropBlockGroup = BlockGroup(BlockGroup.DROP, BLOCK_SIZE_W, BLOCK_SIZE_H, conf, self.getRelPos())

    def update(self):
        if self.isGameOver:
            return
        self.checkGameOver()
        self.fixedBlockGroup.update()
        if self.fixedBlockGroup.IsEliminating():
            return
        if self.dropBlockGroup:
            self.dropBlockGroup.update()
        else:
            self.generateDropBlockGroup()
        if self.willCollide():
            blocks = self.dropBlockGroup.getBlocks()
            for blk in blocks:
                self.fixedBlockGroup.addBlock(blk)
            self.dropBlockGroup.clearBlocks()
            self.dropBlockGroup = None
            self.fixedBlockGroup.processEliminate()

    def draw(self):
        self.fixedBlockGroup.draw(self.surface)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.surface)
        if self.isGameOver:
            rect = self.gameOverImage.get_rect()
            rect.center = (GAME_WIDTH_SIZE // 2, GAME_HEIGHT_SIZE // 2)
            self.surface.blit(self.gameOverImage, rect)
        else:
            self.generateDropBlockGroup

    def getRelPos(self):
        return (240, 50)

    def willCollide(self):
        hash = {}
        allIndex = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndex:
            hash[idx] = 1
        dropIndexes = self.dropBlockGroup.getNextBlockIndexes()
        for dropIndex in dropIndexes:
            if hash.get(dropIndex):
                return True
            if dropIndex[0] >= GAME_ROW:
                return True
        return False

    def checkGameOver(self):
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            if idx[0] < 2:
                self.isGameOver = True
