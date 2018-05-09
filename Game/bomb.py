import pygame, sys, time, random
from pygame.locals import *
from win32api import GetSystemMetrics
import os

def print_text(font, x, y, text, clr=(255, 255, 255)):
    imgtext = font.render(text, True, clr)
    screen.blit(imgtext, (x, y))


def getbombx():
    return random.randint(10, screenwidth - 100)


# print(GetSystemMetrics(0), GetSystemMetrics(1))

bkmusicname = "data\奔跑音乐.mp3"
pygame.mixer.init()
pygame.time.delay(1000)#等待1秒让mixer完成初始化

bkmusic = pygame.mixer.music
bkmusic.load(bkmusicname)
bkmusic.play(loops=-1)
#第一个参数为播放次数，如果是-1表示循环播放，省略表示只播放1次。第二个参数和第三个参数分别表示播放的起始和结束位置

addnusicname = "data\击中.wav"
smusic = pygame.mixer.Sound(addnusicname)

diemusicname = "data\挂了2.wav"
diemusic = pygame.mixer.Sound(diemusicname)

levelmusicname = "data\升级2.wav"
levelmusic = pygame.mixer.Sound(levelmusicname)

overmusicname = "data\over.wav"
overmusic = pygame.mixer.Sound(overmusicname)


floge = 0
#FULLSCREEN
screenwidth = 1280
screenheith = 718
# screenwidth = GetSystemMetrics(0)
# print(screenwidth)
# screenheith = GetSystemMetrics(1)
# print(screenheith)

pygame.init()
# screen = pygame.display.set_mode((600, 500))
bestdepth = pygame.display.mode_ok((screenwidth, screenwidth), floge)  # 传入分辨率with,heith返回这个分辨率在本机上最好的颜色深度
screen = pygame.display.set_mode((screenwidth, screenheith), floge, bestdepth)
pygame.display.set_caption("炸弹游戏")


background_image_filename = "data\背景.jpg"
background = pygame.image.load(background_image_filename).convert() #加载背景图片
# pygame.transform.scale(background, (screenwidth, screenheith))
background = pygame.transform.scale(background,(screenwidth,screenheith))

font1 = pygame.font.SysFont("幼圆", 24)
font2 = pygame.font.SysFont("幼圆", 60)
fontadd = pygame.font.SysFont("幼圆", 100)
white = 255, 255, 255
yellow = 230, 230, 50
red = 220, 50, 50
black = 0, 0, 0

lives = 3
score = 0
game_over = True
mouse_x = moust_y = 0
pos_x = screenwidth / 2
pos_y = screenheith - 40
bomb_x = getbombx()
bomb_y = -50
vel_y = 0.8*screenwidth/500
showTimes = 0
showLives = 0
showLevels = 0
restrart = 0
highscore = 0
prehighcore = 0
level = 1
levelscore = 100





while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        # elif event.type == MOUSEMOTION:
        #     mouse_x, moust_y = event.pos
        #     move_x, move_y = event.rel
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if game_over:
                    game_over = False
                    lives = 3
                    prehighcore = highscore
                    if score > highscore:
                        highscore = score
                    score = 0
                    level = 1
                    pos_x = screenwidth / 2
                    pos_y = screenheith - 40
                    levelscore = 100
                    vel_y = 0.7*screenwidth/500
                    bkmusic.play(loops=-1)

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if keys[K_a]:
        pos_x -= 5
    elif keys[K_d]:
        pos_x += 5
    elif keys[K_LEFT]:
        pos_x -= 5
    elif keys[K_RIGHT]:
        pos_x += 5
    elif keys[K_UP]:
        pos_y -= 5
    elif keys[K_DOWN]:
        pos_y += 5

    # 隐藏鼠标
    pygame.mouse.set_visible(False)

    screen.fill((0, 0, 100))
    screen.blit(background, (0, 0))

    if game_over:
        if restrart == 0:
            print_text(font2, screenwidth/2-150, 200, "点击空格开始!")
        else:
            print_text(font2, screenwidth/2-180, 100, "游戏结束 !")
            print_text(font2, screenwidth/2-200, 180, "本次分数是 " + str(score))
            if score > prehighcore:
                print_text(font2, screenwidth/2-230, 260, "超越历史最高分 " + str(prehighcore))
            print_text(font2, screenwidth/2-200, 420, "点击空格重新开始？")

    else:
        bomb_y += vel_y

        if score >= levelscore:
            vel_y += 0.1*screenheith/500
            level += 1
            levelscore += 100
            levelmusic.play()
            showLevels = 20

        if bomb_y > pos_y+10:#未命中
            print(bomb_y, pos_y)
            bomb_x = random.randint(10, screenwidth - 100)
            bomb_y = -50*screenheith/500
            lives -= 1
            showTimes = 0
            showLives = 20
            diemusic.play()
            if lives == 0:
                game_over = True
                restrart = 1
                bkmusic.stop()
                overmusic.play()
        elif bomb_y > pos_y:#命中
            if bomb_x > pos_x and (bomb_x < pos_x + 120):
                score += 10
                bomb_x = random.randint(10, screenwidth - 100)
                bomb_y = -50
                showTimes = 20
                smusic.play()

        if showTimes > 1:
            if bomb_y < 300:
                print_text(fontadd, screenwidth-200, 100, "+10", red)

        if showLives > 1:
            if bomb_y < 300:
                print_text(font2, screenwidth/2-100, 200, "还有" + str(lives) + "机会", red)
            else:
                showLives = 0
        if showLevels > 1:
            if bomb_y < screenheith / 2:
                print_text(fontadd, 20, 120, "升级啦", red)
            else:
                showLevels = 0


        pygame.draw.circle(screen, black, (bomb_x, int(bomb_y) - 2), 30, 0)
        pygame.draw.circle(screen, yellow, (bomb_x, int(bomb_y)), 30, 0)

        # pos_x = mouse_x
        if pos_x < 0:
            pos_x = 0
        elif pos_x > screenwidth-100:
            pos_x = screenwidth-100
        if pos_y < 100:
            pos_y = 100
        elif pos_y > screenheith-40:
            pos_y = screenheith-40

        pygame.draw.rect(screen, black, (pos_x -2, pos_y - 2, 124, 42), 0)
        pygame.draw.rect(screen, red, (pos_x, pos_y, 120, 40), 0)

    print_text(font1, 5, 2, "分数：" + str(score))
    if score > highscore:
        highscore = score
    print_text(font1, 5, 30, "历史最高分：" + str(highscore))
    print_text(font1, 5, 60, "第" + str(level) + "关")
    print_text(font1, screenwidth-100, 2, "剩余: " + str(lives))



    pygame.display.update()
