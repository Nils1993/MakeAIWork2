from Neuroot import Neuroot
import random
import numpy as np
import math

# Creating shapes
cross01 = [
    [1,0,1],
    [0,1,0],
    [1,0,1],
]

cross02 = [
    [0,1,0],
    [1,1,1],
    [0,1,0]
]

circle01 = [
    [0,1,0],
    [1,0,1],
    [0,1,0]
]

circle02 = [
    [1,1,1],
    [1,0,1],
    [1,1,1]
]

x_cross = cross01, cross02
x_circle = circle01, circle02
y_cross = [1]
y_circle = [0]

circle = Neuroot()
cross = Neuroot()

circle.train(x_circle, y_circle)


