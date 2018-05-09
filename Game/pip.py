import pygame, sys
import math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("小游戏，按1,2,3,4")
myfont = pygame.font.Font(None, 60)

color = 200, 80, 60
width = 4
x = 300
y = 250
radius = 200
position = x-radius, y-radius, radius*2, radius*2

piecel1 = False
piecel2 = False
piecel3 = False
piecel4 = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_1:
                piecel1 = True
            elif event.key == pygame.K_2:
                piecel2 = True
            elif event.key == pygame.K_3:
                piecel3 = True
            elif event.key == pygame.K_4:
                piecel4 = True

    screen.fill((0, 0, 200))

    textImg1 = myfont.render("1", True, color)
    screen.blit(textImg1, (x+radius/2-20, y-radius/2))
    textImg2 = myfont.render("2", True, color)
    screen.blit(textImg2, (x-radius/2, y-radius/2))
    textImg3 = myfont.render("3", True, color)
    screen.blit(textImg3, (x-radius/2, y+radius/2-20))
    textImg4 = myfont.render("4", True, color)
    screen.blit(textImg4, (x+radius/2-20, y+radius/2-20))

    if piecel1:
        start_angle = math.radians(0)
        end_angle = math.radians(90)
        pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x, y), (x, y-radius), width)
        pygame.draw.line(screen, color, (x, y), (x+radius, y), width)
    if piecel2:
        start_angle = math.radians(90)
        end_angle = math.radians(180)
        pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x, y), (x, y-radius), width)
        pygame.draw.line(screen, color, (x, y), (x-radius, y), width)
    if piecel3:
        start_angle = math.radians(180)
        end_angle = math.radians(270)
        pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x, y), (x-radius, y), width)
        pygame.draw.line(screen, color, (x, y), (x, y+radius), width)
    if piecel4:
        start_angle = math.radians(270)
        end_angle = math.radians(360)
        pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x, y), (x+radius, y), width)
        pygame.draw.line(screen, color, (x, y), (x, y+radius), width)

    if piecel1 and piecel2 and piecel3 and piecel4:
            color = 0, 255, 0

    pygame.display.update()