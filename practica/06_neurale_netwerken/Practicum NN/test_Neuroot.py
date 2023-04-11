from Neuroot import Neuroot
import random
import numpy as np
import math

# Creating shapes
cross01 = [
    [1,0,1],
    [0,1,0],
    [1,0,1]
]

cross02 = [
    [0,1,0],
    [1,1,1],
    [0,1,0]
]
cross03 = [
    [0,1,0],
    [1,1,0],
    [0,1,0]
]
cross04 = [
    [0,0,1],
    [0,1,0],
    [1,0,1]
]
cross05 = [
    [1,0,1],
    [0,1,0],
    [0,0,1]
]
cross06 = [
    [1,0,1],
    [0,1,0],
    [1,0,0]
]
cross07 = [
    [1,0,0],
    [0,1,0],
    [1,0,1]
]
cross08 = [
    [0,0,0],
    [1,1,1],
    [0,1,0]
]
cross09 = [
    [0,1,0],
    [0,1,1],
    [0,1,0]
]
cross10 = [
    [0,1,0],
    [1,1,1],
    [0,0,0]
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

circle03 = [
    [0,1,0],
    [1,0,1],
    [0,0,0]
]

circle04 = [
    [1,1,1],
    [1,0,1],
    [1,0,1]
]
circle05 = [
    [1,1,1],
    [1,0,0],
    [1,1,1]
]
circle06 = [
    [1,0,1],
    [1,0,1],
    [1,1,1]
]
circle07 = [
    [1,1,1],
    [0,0,1],
    [1,1,1]
]
circle08 = [
    [0,1,0],
    [1,0,0],
    [0,1,0]
]
circle09 = [
    [0,0,0],
    [1,0,1],
    [0,1,0]
]
circle10 = [
    [0,1,0],
    [0,0,1],
    [0,1,0]
]










# x_cross = cross01, cross02
# x_circle = circle01, circle02
# y_cross = [1]
# y_circle = [0]
y_data = [[0,1], [0,1], [0,1], [0,1], [1,0], [1,0], [1,0], [1,0]]
x_data = cross01, cross02, cross03, cross04, circle01, circle02, circle03, circle04

test = Neuroot()

test.train(x_data, y_data, epochs=100000)
test.predict(cross01)
test.predict(cross02)
test.predict(cross03)
test.predict(cross04)
test.predict(circle01)
test.predict(circle02)
test.predict(circle03)
test.predict(circle04)




