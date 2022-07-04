import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image as Image
import math
import numpy


class Model:
    def __init__(self, filepath):
        self.filepath = filepath