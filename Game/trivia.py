import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600,500))
pygame.display.set_caption(u"答题游戏")
font1 = pygame.font.SysFont("华文中宋", 40)
# font1 = pygame.font.Font(None, 40)
font2 = pygame.font.SysFont("华文中宋", 24)
white = 255, 255, 255
cyan = 0, 255, 255
yellow = 255, 255, 0
purple = 255, 0, 255
green = 0, 255, 0
red = 255, 0, 0


class Trivia(object):
    def __init__(self, filename):
        self.data = []
        self.current = 0
        self.total = 0
        self.correct = 0
        self.score = 0
        self.scored = False
        self.failed = False
        self.wronganswer = 0
        self.colors = [white, white, white, white]

        f = open(filename, "r")
        trivia_data = f.readlines()
        f.close()

        for text_line in trivia_data:
            self.data.append(text_line.strip())
            self.total += 1

    def print_text(self, ft, x, y, txt, clr=(255, 255, 255), shadow=True):
        if shadow:
            imgtext = ft.render(txt, True, (0, 0, 0))
            screen.blit(imgtext, (x-2, y-2))
        imgeText = ft.render(txt, True, clr)
        screen.blit(imgeText, (x, y))

    def show_question(self):
        self.print_text(font1, 210, 5, "答题游戏")
        self.print_text(font2, 210, 500-30, "请按1-4来答题", purple, False)
        self.print_text(font2, 530, 10, "分数", purple, False)
        self.print_text(font2, 550, 35, str(self.score), purple, False)

        # 正确答案
        self.correct = int(self.data[self.current + 5])

        question = self.current // 6 + 1
        self.print_text(font1, 5, 80, "问题" + str(question))
        self.print_text(font2, 20, 130, self.data[self.current], yellow)

        if self.scored:
            self.colors = [white, white, white, white]
            self.colors[self.correct - 1] = green
            if self.current + 6 >= self.total:
                self.print_text(font1, 50, 380, "回答正确,总分：{}，正确：{}".format(self.total//6, self.score), green)
                self.print_text(font2, 175, 428, "请按回车键重新开始", green)
            else:
                self.print_text(font1, 230, 380, "回答正确", green)
                self.print_text(font2, 175, 428, "请按回车键开始下一题", green)
        elif self.failed:
            self.colors = [white, white, white, white]
            self.colors[self.correct - 1] = green
            self.colors[self.wronganswer - 1] = red
            if self.current + 6 >= self.total:
                self.print_text(font1, 50, 380, "回答正确,总分：{}，正确：{}".format(self.total//6, self.score), green)
                self.print_text(font2, 175, 428, "请按回车键重新开始", green)
            else:
                self.print_text(font1, 230, 380, "回答错误", red)
                self.print_text(font2, 175, 428, "请按回车键开始下一题", green)
        self.print_text(font1, 5, 170, "选项：")
        self.print_text(font2, 20, 230, "1-" + self.data[self.current + 1], self.colors[0])
        self.print_text(font2, 20, 260, "2-" + self.data[self.current + 2], self.colors[1])
        self.print_text(font2, 20, 290, "3-" + self.data[self.current + 3], self.colors[2])
        self.print_text(font2, 20, 320, "4-" + self.data[self.current + 4], self.colors[3])

    def handle_input(self, number):
        if not self.scored and not self.failed:
            if number == self.correct:
                self.scored = True
                self.score += 1
            else:
                self.failed = True
                self.wronganswer = number

    def next_question(self):
        if self.scored or self.failed:
            self.scored = False
            self.failed = False
            self.correct = 0
            self.colors = [white, white, white, white]
            self.current += 6
            if self.current >= self.total:
                self.current = 0
                self.score = 0

triObj = Trivia("timu.txt")

print(triObj.data)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_1:
                triObj.handle_input(1)
            elif event.key == pygame.K_2:
                triObj.handle_input(2)
            elif event.key == pygame.K_3:
                triObj.handle_input(3)
            elif event.key == pygame.K_4:
                triObj.handle_input(4)
            elif event.key == pygame.K_RETURN:
                triObj.next_question()

    screen.fill((0, 0, 200))

    triObj.show_question()

    pygame.display.update()
