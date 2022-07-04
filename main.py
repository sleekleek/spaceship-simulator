import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glm

from camera import Camera
from model import Model
from planet import Planet


NAME = 'Fly Me To The Moon'
WIDTH, HEIGHT = 1400, 800

planets = []

def main():
    glutInit()  # Initialize a glut instance which will allow us to customize our window
    glutInitDisplayMode(GLUT_RGBA)  # Set the display mode to be colored
    glutInitWindowSize(WIDTH, HEIGHT)   # Set the width and height of your window
    # Set the position at which this windows should appear
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(NAME)  # Give your window a title
    # Tell OpenGL to call the displayScreen method continuously
    glutDisplayFunc(displayScreen)
    # Draw any graphics or shapes in the displayScreen function at all times
    glutIdleFunc(displayScreen)
    glutMainLoop()  # Keeps the window created above displaying/running in a loop

    # Load models
    

    cam = Camera()


def displayScreen():
    #TODO
    pass

if __name__ == '__main__':
    main()