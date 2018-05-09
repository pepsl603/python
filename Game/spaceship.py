import pygame, sys, random, math, copy
from pygame.locals import *


class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def getx(self):
        return self.__x

    def setx(self, x):
        self.__x = x
    x = property(getx, setx)

    def gety(self):
        return self.__y

    def sety(self, y):
        self.__y = y
    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
                ",Y:" + "{:.0f}".format(self.__y) + "}"


def print_text(font, x, y, text, clr=(255, 255, 255)):
    imgtext = font.render(text, True, clr)
    screen.blit(imgtext, (x, y))


pygame.init()
dlgwidth = 1024
dlgheight = 768
screen = pygame.display.set_mode((dlgwidth, dlgheight))
pygame.display.set_caption("星空模型")
font = pygame.font.Font(None, 24)

# 星空背景
space = pygame.image.load("data\space.jpg").convert()

#星球
planet = pygame.image.load("data\planetnew.png").convert_alpha()
planet_with, planet_height = 400, 400
#341, 227
# planet_with, planet_height = planet.get_size()
# planet_with, planet_height = int(planet_with / 1.6), int(planet_height / 1.6)
# print(planet_with, planet_height)
planet = pygame.transform.smoothscale(planet, (planet_with, planet_height))
#更加平滑
#星球位置
planet_pos = (dlgwidth/2 - planet_with/2, dlgheight/2 - planet_height/2)

#飞船
ship = pygame.image.load("data\ship.png").convert_alpha()
ship_width, ship_height = 128, 128
ship = pygame.transform.smoothscale(ship, (ship_width, ship_height))

ship = pygame.transform.rotate(ship, 110)

#旋转轨道
pos = Point(0, 0)
old_pos = Point(0, 0)
radius = 300
angle = 0.0
white = 255, 255, 255
clr = 255, 255, 255
lst_clr = 255, 255, 255

speed = 0.1
his_points = []
tmp_points = []
his_number = 0
his_max = 5000
num = 0
rep_flag = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                speed = 0.1
        keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if keys[K_SPACE]:
        speed += 0.001
        if speed > 1.0:
            speed = 1

    screen.blit(space, (0, 0))
    screen.blit(planet, planet_pos)


    #旋转船
    angle += speed
    if angle % 360 == 0:
        angle == 0
    pos.x = math.cos(math.radians(angle)) * radius
    pos.y = math.sin(math.radians(angle)) * radius

    rangle = math.atan2(pos.y, pos.x)
    rangled = math.degrees(-rangle)
    scratch_ship = pygame.transform.rotate(ship, rangled)

    # delta_x = (pos.x - old_pos.x)
    # delta_y = (pos.y - old_pos.y)
    # rangle = math.atan2(delta_y, delta_x)
    # rangled = math.degrees(-rangle + 90)
    # print(rangled%360)
    # scratch_ship = pygame.transform.rotate(ship, rangled)



    scratch_ship_with, scratch_ship_height = scratch_ship.get_size()

    x = dlgwidth/2 + pos.x - scratch_ship_with/2
    y = dlgheight/2 + pos.y - scratch_ship_height/2

    if angle % 360 > 1:
        rep_flag = 0
        for pt in tmp_points:
            pygame.draw.circle(screen, lst_clr, (int(pt.x), int(pt.y)), 5, 0)
        for pt in his_points:
            pygame.draw.circle(screen, clr, (int(pt.x), int(pt.y)), 5, 0)
    else:
        if rep_flag == 0:
            rep_flag = 1
            lst_clr = clr
            clr = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            tmp_points.clear()
            tmp_points = copy.deepcopy(his_points)
            his_points.clear()



    screen.blit(scratch_ship, (x, y))

    pygame.display.update()
    old_pos.x = pos.x
    old_pos.y = pos.y

    if len(his_points) < his_max:
        tmp_pos = Point(0, 0)
        tmp_pos.x = dlgwidth / 2 + pos.x
        tmp_pos.y = dlgheight / 2 + pos.y
        his_points.append(tmp_pos)
    else:
        his_points[his_number].x = dlgwidth / 2 + pos.x
        his_points[his_number].y = dlgheight / 2 + pos.y
        his_number += 1
        if his_number == his_max:
            his_number = 0
