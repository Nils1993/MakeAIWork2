import pygame
from copy import deepcopy
from random import choice, randrange
import numpy as np
from tetris_objects import Figure

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

# Tetris objects
# Replace by classfigure
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]
               

figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

bg = pygame.image.load('img/bg.jpg').convert()
game_bg = pygame.image.load('img/bg2.jpg').convert()

main_font = pygame.font.Font('font/font.ttf', 65)
font = pygame.font.Font('font/font.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = Figure(choice(figures_pos)), Figure(choice(figures_pos))
color, next_color = figure.getColor(), next_figure.getColor()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if figure.shape[i].x < 0 or figure.shape[i].x > W - 1:
        return False
    elif figure.shape[i].y > H - 1 or field[figure.shape[i].y][figure.shape[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure.shape[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure.shape[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old.shape[i].y][figure_old.shape[i].x] = color
                figure, color = next_figure, next_color
                next_figure = Figure(choice(figures_pos))
                next_color = next_figure.getColor()
                anim_limit = 2000
                break
    # rotate
    center = figure.shape[0]
    figure_old = deepcopy(figure)
    if rotate:
        figure.rotate(figure_old)

    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
    # compute score
    score += scores[lines]
    # draw grid
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # draw figure
    for i in range(4):
        figure_rect.x = figure.shape[i].x * TILE
        figure_rect.y = figure.shape[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    # draw next figure
    for i in range(4):
        figure_rect.x = next_figure.shape[i].x * TILE + 380
        figure_rect.y = next_figure.shape[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)
    # draw titles
    sc.blit(title_tetris, (485, -10))
    sc.blit(title_score, (535, 780))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 840))
    sc.blit(title_record, (525, 650))
    sc.blit(font.render(record, True, pygame.Color('gold')), (550, 710))
    # game over
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)