import pygame
import sys
from pygame.locals import *

pygame.init()

DISPALYSURF = pygame.display.set_mode((800, 600))


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("yellow.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            self.rect.move_ip(-1, 0)
        elif pressed[K_RIGHT]:
            self.rect.move_ip(1, 0)
        elif pressed[K_UP]:
            self.rect.move_ip(0, -1)
        elif pressed[K_DOWN]:
            self.rect.move_ip(0, 1)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


B = Block()  # 生成一个类的实例

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    B.update()  # 调用update()方法更新方块的位置问题出在
   # B.update=()这一行。这行代码将B.update属性设置为一个空元组，而不是调用B.update()方法来更新方块的位置

    DISPALYSURF.fill((0, 0, 0))  # (0,0,0)代表黑色的RGB值
    B.draw(DISPALYSURF)

    pygame.display.update()


    # def __init__(self,blockType,pos):执行初始化参数
    #     super().__init__()
#    self.image=pygame.image.load(BLOCK_RES[blockType])
#         self.rect=self.image.get_rect()
#         self.rect.center= pos


# P=Block(BlockType.PURPLE,(200,300))
# G=Block(BlockType.GREEN,(600,300))



#    P.update()
#         G.update()


        #     P.draw(DISPALYSURF)
        # G.draw(DISPALYSURF)
