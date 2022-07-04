import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image as Image
import math
import numpy

from model import Model


class Planet(Model):
    def __init__(self, filepath, rotateSpeed=5e-5):
        super().__init__(filepath)
        self.angle = 0
        self.rotateSpeed = rotateSpeed