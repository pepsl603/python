import pygame, sys, time, random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("炸弹游戏")

font1 = pygame.font.Font(None, 24)
font2 = pygame.font.Font(None, 200)
white = 255, 255, 255
yellow = 255, 255, 0

key_flag = False
correct_answer = 97
seconds = 11
score = 0
clock_start = 0
game_over = True


def print_text(font, x, y, text, clr=(255, 255, 255)):
    imgtext = font.render(text, True, clr)
    screen.blit(imgtext, (x, y))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            key_flag = True
        elif event.type == KEYUP:
            key_flag = False

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if keys[K_RETURN]:
        if game_over:
            game_over = False
            score = 0
            seconds = 11
            clock_start = time.clock()

    # clock_start = time.clock()
    current = time.clock() - clock_start
    speed = score * 6
    if seconds - current < 0:
        game_over = True
    elif current <= 10:
        if keys[correct_answer]:
            correct_answer = random.randint(97, 122)
            score += 1
            clock_start = time.clock()
    screen.fill((0, 100, 0))

    print_text(font1, 0, 0, "Let's see how fast you can type!")
    print_text(font1, 0, 20, "Try to keep up for 10 seconds...")

    if key_flag:
        print_text(font1, 500, 0, "<key>")

    print_text(font1, 0, 40, "currenttime:" + str(current))
    print_text(font1, 0, 60, "starttime:" + str(clock_start))
    if not game_over:
        print_text(font1, 0, 80, "Time:" + str(int(seconds - current)))
    print_text(font1, 0, 100, "Speed:" + str(speed) + " letters/min")

    if game_over:
        print_text(font1, 0, 160, "Press Enter to start...")

    print_text(font2, 0, 240, chr(correct_answer - 32), yellow)

    pygame.display.update()


# pygame.key.set_repeat(100)
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             sys.exit()
#         elif event.type == KEYDOWN:
#             if event.key == K_ESCAPE:
#                 sys.exit()
#             else:
#                 print(event.key)
#         elif event.type == MOUSEMOTION:
#             mouse_x, mouse_y = event.pos
#             move_x, move_y = event.rel
#         elif event.type == MOUSEBUTTONDOWN:
#             mouse_down = event.button
#             mouse_down_x, mouse_down_y = event.pos
#         elif event.type == MOUSEBUTTONUP:
#             mouse_up = event.button
#             mouse_up_x, mouse_up_y = event.pos
#



