from world import World
from initialParams import *
from turtle import *
import pygame


def main():
    # 初始化 Pygame
    pygame.init()

    # 网格设置
    GRID_SIZE = 40
    NUM_GRIDS = 40
    SCREEN_WIDTH = GRID_SIZE * NUM_GRIDS
    SCREEN_HEIGHT = GRID_SIZE * NUM_GRIDS

    # 设置窗口大小
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 定义颜色
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)  # 代表代理
    BLUE = (0, 0, 255)  # 代表警察
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # 游戏循环标志
    running = True

    print("program Started")
    world = World(agent_density=INITIAL_AGENT_DENSITY, cop_density=INITIAL_COP_DENSITY, vision=VISION_PATCHES)
    tick = 0

    # 游戏循环
    while running:
        print("Tick " + str(tick))
        s = world.update()

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if tick == MAX_TICK:
                running = False

        # 填充背景色
        screen.fill(WHITE)

        # 绘制网格（可选）
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 1)

        tempCop = 0
        # 绘制代理和警察
        for i in s:
            if isinstance(i, Agent):
                if i.jail_term > 0:
                    pygame.draw.circle(screen, BLACK,
                                       (i.x * GRID_SIZE + GRID_SIZE // 2, i.y * GRID_SIZE + GRID_SIZE // 2),
                                       GRID_SIZE // 2 - 5)
                elif i.active:
                    pygame.draw.circle(screen, RED,
                                       (i.x * GRID_SIZE + GRID_SIZE // 2, i.y * GRID_SIZE + GRID_SIZE // 2),
                                       GRID_SIZE // 2 - 5)
                else:
                    pygame.draw.circle(screen, GREEN, (i.x * GRID_SIZE + GRID_SIZE // 2, i.y * GRID_SIZE + GRID_SIZE // 2),
                                    GRID_SIZE // 2 - 5)

        for i in s:
            if isinstance(i, Cop):
                pygame.draw.circle(screen, BLUE, (i.x * GRID_SIZE + GRID_SIZE // 2, i.y * GRID_SIZE + GRID_SIZE // 2),
                                   GRID_SIZE // 2 - 5)
                tempCop += 1

        # 更新屏幕
        pygame.display.flip()

        # 控制游戏更新速度
        pygame.time.Clock().tick(5)
        #print("Cop: " + str(tempCop))
        tick += 1
    # 退出 Pygame
    pygame.quit()
    print("program Ended")


if __name__ == '__main__':
    main()
