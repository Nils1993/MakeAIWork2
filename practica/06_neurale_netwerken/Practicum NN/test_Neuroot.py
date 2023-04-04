from Neuroot import Neuroot
import random

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


test = Neuroot()

test.classify(cross01)

