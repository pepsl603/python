import pygame, sys
import math,random
from pygame.locals import *

pygame.init()

ZiTi= pygame.font.get_fonts()
for i in ZiTi:
   print(i)

screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("测试游戏")

myfont = pygame.font.SysFont("幼圆", 60)

white = 255, 255, 255
blue = 0, 0, 255
# #画字
# Boy,Press any key to go on
textImage = myfont.render('靓仔，按任意键开始', True, white)
screen.fill(blue)
screen.blit(textImage, (20, 100))
pygame.display.update()

waitFlag = True
while waitFlag:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            print('开始！')
            waitFlag = False

pos_x = 300
pos_y = 250
vel_x = 2
vel_y = 1

while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    # #画字
    # textImage = myfont.render("Hello Pygame", True, white)
    # screen.fill(blue)
    # screen.blit(textImage, (100, 100))

    screen.fill(blue)

    # 画圆
    color = 255, 255, 0
    position = 300, 250
    radius = 50
    width = 5
    pygame.draw.circle(screen, color, position, radius, width)

    # 画移动的圆
    pos_x += vel_x
    pos_y += vel_y
    if pos_x > 500 or pos_x < 0:
        vel_x = -vel_x
    if pos_y > 400 or pos_y < 0:
        vel_y = -vel_y
    color = 255, 255, 0
    width = 0
    pos = pos_x, pos_y, 100, 100
    pygame.draw.rect(screen, color, pos, width)

    # 画线
    pygame.draw.line(screen, color, (300, 250), (pos_x, pos_y), 5)

    rx = random.randint(0,500)
    ry = random.randint(0,400)
    rcolor = random.randint(0,255), random.randint(0,255), random.randint(0,255)
    pygame.draw.line(screen, rcolor, (300, 250), (rx, ry), 5)

    # 画弧形
    pos = 225, 300, 150, 150
    start_angle = math.radians(0)
    end_angle = math.radians(180)
    pygame.draw.arc(screen, color, pos, start_angle, end_angle, 5)

    #刷新画布
    pygame.display.update()
