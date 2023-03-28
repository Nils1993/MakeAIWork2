#!/usr/bin/env python

from tetris_objects import Figure
from random import choice, randrange
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG)

# iShape

# Shape of i-shape
shape = np.array([(-1, 0), (-2, 0), (0, 0), (1, 0)])

# Random Red Green Blue Color
color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

iShape = Figure(shape, color)

logging.debug(f"iShape color : {iShape.getColor()}")
logging.debug(f"iShape shape :  {iShape.getShape()}")

logging.debug("Rotate counterclockwise")
iShape.rotate()

logging.debug(f"iShape color : {iShape.getColor()}")
logging.debug(f"iShape shape :  {iShape.getShape()}")

shape = np.array(
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
)
zShape = Figure(shape, color)
zShape.rotate()
