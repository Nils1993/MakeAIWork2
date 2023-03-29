import pygame
from random import randrange
from copy import deepcopy

"""
Classnames always UpperCamelCase
"""

W,H = 10, 20

field = [[0 for i in range(W)] for j in range(H)]

class Figure:
    # Constructor method
    def __init__(self, shape):
        self.shape = [pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in shape]

    
    # Returns Shape
    def getShape(self):
        return self.shape
    
    # Returns attribute color
    def getColor(self):
        return (randrange(30, 256), randrange(30, 256), randrange(30, 256))

    # Change shape by multiplying with Numpy Array
    # self.shape gets new shape
    # Counter clockwise
    def rotate(self, shape_old):
        center = self.shape[0]

        for i in range(4):
            x = self.shape[i].y - center.y
            y = self.shape[i].x - center.x
            self.shape[i].x = center.x - x
            self.shape[i].y = center.y + y
            if not self.check_borders(i):
                self.shape = deepcopy(shape_old.shape)
                break

    def check_borders(self, i):
        if self.shape[i].x < 0 or self.shape[i].x > W - 1:
            return False
        elif self.shape[i].y > H - 1 or field[self.shape[i].y][self.shape[i].x]:
            return False
        return True