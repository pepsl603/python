import pygame, sys, math, random
from pygame.locals import *
from datetime import  datetime, date, time


def print_text(font, x, y, text, clr=(255, 255, 255)):
    imgtext = font.render(text, True, clr)
    screen.blit(imgtext, (x, y))


pygame.init()

screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("时钟")
font = pygame.font.Font(None, 36)
screen.fill((0, 0, 0))

orange = 220, 180, 0
yellow = 255, 255, 0
pink = 255, 100, 100
white = 255, 255, 255
pos_x = 300
pos_y = 250
radius = 240
angle = 360


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            sys.exit()

    screen.fill((0, 0, 0))
    angle += 1
    if angle >= 360:
        angle = 0

    ptick = pygame.time.Clock().tick(30)
    print(ptick)

    today = datetime.now()
    hours = today.hour % 12
    minutes = today.minute
    minhour = minutes % 5
    seconds = today.second

    screen.fill((0, 0, 0))
    print_text(font,1,1,datetime.now().strftime("%H:%M:%S"))

    # 画时针
    hour_angle = 360 * (hours / 12) + (minutes/60) * (360 / 12 / 5) - 90
    hour_x = math.cos(math.radians(hour_angle)) * (radius-80)
    hour_y = math.sin(math.radians(hour_angle)) * (radius-80)
    hourpos = (pos_x + hour_x, pos_y + hour_y)
    pygame.draw.line(screen, pink, (pos_x, pos_y), hourpos, 25)

    # 画分针
    # print(minutes)
    minute_angle = 360 * minutes / 60 - 90
    minute_x = math.cos(math.radians(minute_angle)) * (radius-60)
    minute_y = math.sin(math.radians(minute_angle)) * (radius-60)
    minute_pos = (pos_x + minute_x, pos_y + minute_y)
    pygame.draw.line(screen, orange, (pos_x, pos_y), minute_pos, 15)

    # 画秒针
    # print(minutes)
    second_angle = 360 * seconds / 60 - 90
    second_x = math.cos(math.radians(second_angle)) * (radius-40)
    second_y = math.sin(math.radians(second_angle)) * (radius-40)
    second_pos = (pos_x + second_x, pos_y + second_y)
    pygame.draw.line(screen, yellow, (pos_x, pos_y), second_pos, 5)

    # 画中心点
    pygame.draw.circle(screen, white,(pos_x,pos_y),15,0)

    # 画表框
    pygame.draw.circle(screen, white, (pos_x, pos_y), radius, 10)

    # 画表盘
    for i in range(1, 13):
        angle = math.radians(360 * i / 12 - 90)
        # x = math.cos(angle) * (radius - 20) - 10
        # y = math.sin(angle) * (radius - 20) - 10
        # print_text(font, pos_x+x, pos_y+y, str(i))
        x = math.cos(angle) * (radius - 20)
        y = math.sin(angle) * (radius - 20)
        pygame.draw.circle(screen, yellow, (int(pos_x+x),int( pos_y+y)), 5, 0)
        x = math.cos(angle) * (radius - 40)
        y = math.sin(angle) * (radius - 40)
        # pygame.draw.circle(screen, yellow, (int(pos_x + x), int(pos_y + y)), 5, 0)
        print_text(font, pos_x + x - 8, pos_y + y-10, str(i))

    pygame.display.update()