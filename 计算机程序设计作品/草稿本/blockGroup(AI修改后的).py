import random
from typing import Any
import pygame
import sys
from pygame.locals import *
from block import *
from const import *
from utiles import *


class BlockGroup(object):
    DROP = 1
    BLOCKMAX = 5 
    # Add other block group types here

    def GenerateBlockGroupConfig(rowIdx, colIdx):
        shapeIdx = random.randint(0, len(BLOCK_SHAPE) - 1)
        bType = random.randint(0, BlockType.BLOCKMAX - 1)
        configList = []
        rotIdx = 0
        for i in range(len(BLOCK_SHAPE[shapeIdx][rotIdx])):
            config = {
                'blockType': bType,
                'blockShape': shapeIdx,
                'blockRot': rowIdx,
                'blockGroupIdx': i,
                'rowIdx': rowIdx,
                'colIdx': colIdx,
            }
            configList.append(config)
        return configList

    def __init__(self, blockGroupType, width, height, blockConfigList, relPos):
        super().__init__()
        self.blocks = []
        self.time = 0
        self.pressTime = {}
        self.blockGroupType = blockGroupType
        self.isEliminating = False
        self.dropInterval = 300
        for config in blockConfigList:
            bIk = Block(config["blockType"], config['rowIdx'], config['colIdx'], width, height, relPos)
            self.blocks.append(bIk)

    def draw(self, surface):
        for b in self.blocks:
            b.draw(surface)

    def update(self):
        oldTime = self.time
        curTime = getCurrentTime()
        diffTime = curTime - oldTime
        if self.blockGroupType == BlockGroup.DROP:
            if diffTime >= self.dropInterval:
                self.time = curTime
                for b in self.blocks:
                    b.drop()
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

    def deEliminate(self, row):
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
