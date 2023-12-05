
from const import *
import pygame
from pygame.locals import *
from utiles import *
import pygame,sys



class Block(pygame.sprite.Sprite):
    def __init__(self,blockType,baseRowIdx,baseColIdx,blockGroupIdx,blockRot,blockShape,width,heigh,relPos):
        super().__init__()
        self.blockType=blockType
        self.blockShape=blockShape
        self.blockRot=blockRot
        self.blockGroupIdx=blockGroupIdx
        self.baseRowIdx=baseRowIdx
        self.baseColIdx=baseColIdx
        self.width=width
        self.heigh=heigh
        self.relPos=relPos # 相对位置
        self.blink=False
        self.blinkCount=0
        self.loadImage()
        self.updateImagePos() # 更新图像位置

    def startBlink(self): # 开始闪烁
        self.blink = True
        self.blinkTime= getCurrentTime#GetCurrenTime()
    
    def loadImage(self): # 加载图片
        self.image=pygame.image.load(BLOCK_RES[self.blockType])
        self.image=pygame.transform.scale(self.image,(self.width,self.heigh))
   
    def updateImagePos(self):
        # 更新图像的位置
        self.rect = self.image.get_rect()
        # 图像矩形的位置
        self.rect.left = self.relPos[0] + self.width * self.colIdx
        # 图像矩形的左边界位置
        self.rect.top = self.relPos[1] + self.heigh * self.rowIdx
        # 图像矩形的上边界位置

    def draw(self,surface):
        self.updateImagePos()
        if self.blink and self.blinkCount % 2==0:
           return
        surface.blit(self.image,self.rect)

    def drop(self):
        self.baseRowIdx += 1
       
    
    def getIndex(self):
        return(int(self.rowIdx), int(self.colIdx))
    
    def getNextIndex(self):
         # 获取下一个索引位置并以元组形式返回行索引和列索引
        return(int(self.rowIdx + 1), int(self.colIdx))
         # :return: 下一个索引位置的行索引和列索引的元组

    def ilLeftBound(self):
        return self.colIdx==0
    
    def isRightBound(self):
        return self.colIdx==GAME_COL-1
    
    def doLeft(self):
        self.baseColIdx -= 1
 
    def doRight(self):
        self.baseColIdx += 1

    def getBlockfigIndex(self):
        return BLOCK_SHAPE[self.blockShape][self.blockRot][self.blockGroupIdx]
    
    @property
    def rowIdx(self):
        return self.baseRowIdx + self.getBlockfigIndex()[0]
    
    @property
    def colIdx(self):
        return self.baseColIdx +self.getBlockfigIndex()[1]
    
    def doLeft(self):
        self.baseColIdx -=1

    def doRignt(self):
        self.baseColIdx +=1

    def drop(self):
        self.baseRowIdx +=1

    def doRotate(self):
        self.blockRot += 1
        if self.blockRot >= len(BLOCK_SHAPE[self.blockShape]):
            self.blockRot =  0

    def update(self):
        if self.blink:
            diffTime= getCurrentTime() - self.blinkTime
            self.blinkCount =int(diffTime / 20)