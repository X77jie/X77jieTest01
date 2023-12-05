import pygame,sys
import random

# 初始化Pygame
pygame.init()

# 设置窗口大小
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 创建窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 设置游戏标题
pygame.display.set_caption("Block Fall")

# 设置游戏时钟
clock = pygame.time.Clock()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 定义方块类
class Block:
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(random.randint(0, width), 0, width, height)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# 创建方块对象
blocks = []
for i in range(6):
    block = Block(BLUE, WINDOW_WIDTH // 6, WINDOW_HEIGHT // 5)
    blocks.append(block)

# 定义游戏循环
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # 更新屏幕
    screen.fill(BLACK)
    
    # 绘制方块
    for block in blocks:
        block.draw(screen)
    
    # 刷新屏幕
    pygame.display.flip()
    
    # 控制游戏帧率
    clock.tick(60)