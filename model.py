import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyassimp import * 
from PIL import Image as Image
import math
import numpy


class Model:
    def __init__(self, filepath):
        self.filepath = filepath
        self.texture = self.mapTexture(filepath)
        self.model = self.loadModel(filepath)
    
    
    def loadModel(self):
        scene = load(self.filepath + "/Model.obj")

        assert len(scene.meshes)
        mesh = scene.meshes[0]

        assert len(mesh.vertices)
        print(mesh.vertices[0])

        release(scene)


    def mapTexture(self):
        img = Image.open(self.filepath + "/Texture.jpg")
        img_data = numpy.array(list(img.getdata()), numpy.int8)
        textID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                     img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

        return textID
