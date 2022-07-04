import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image as Image
import math
import numpy


class Planet:
    def __init__(self, filename):
        self.filename = filename
        self.textureId = 0
        self.angle = 0

    def drawSphere(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(math.cos(self.angle)*4, math.sin(self.angle)
                  * 4, 0, 0, 0, 0, 0, 0, 1)
        self.angle += 5e-5
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindTexture(GL_TEXTURE_2D, self.textureId)

        glEnable(GL_TEXTURE_2D)

        qobj = gluNewQuadric()
        gluQuadricTexture(qobj, GL_TRUE)
        gluSphere(qobj, 1, 50, 50)
        gluDeleteQuadric(qobj)

        glDisable(GL_TEXTURE_2D)

        glutSwapBuffers()
        glutPostRedisplay()

    def mapTexture(self):
        img = Image.open(self.filename)
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

    def runScene(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(0, 0)
        glutCreateWindow('Fly Me To The Moon')
        self.textureId = self.mapTexture()
        glutDisplayFunc(self.drawSphere)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(40, 1, 1, 40)
        glutMainLoop()


if __name__ == '__main__':
    moon = Planet('solar_textures/2k_moon.jpg')
    moon.runScene()
