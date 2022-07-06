import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pyassimp 
from PIL import Image as Image
import numpy


class Model:
    def __init__(self, filepath):
        self.filepath = filepath
        self.model = self.loadModel()
        self.texture = self.mapTexture()
    
    
    def loadModel(self):
        scene = pyassimp.load(self.filepath + "Model.obj",
                              processing=pyassimp.postprocess.aiProcess_Triangulate | pyassimp.postprocess.aiProcess_FlipUVs)

        for mesh in scene.meshes:
            self.prepareGlBuffers(mesh)

        pyassimp.release(scene)


    def prepareGlBuffers(self, mesh):
        """ Creates 3 buffer objects for each mesh,
        to store the vertices, the normals, and the faces
        indices.
        """

        mesh.gl = {}

        # Fill the buffer for vertex positions
        mesh.gl["vertices"] = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, mesh.gl["vertices"])
        glBufferData(GL_ARRAY_BUFFER,
                     mesh.vertices,
                     GL_STATIC_DRAW)

        # Fill the buffer for normals
        mesh.gl["normals"] = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, mesh.gl["normals"])
        glBufferData(GL_ARRAY_BUFFER,
                     mesh.normals,
                     GL_STATIC_DRAW)

        # Fill the buffer for vertex positions
        mesh.gl["triangles"] = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.gl["triangles"])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     mesh.faces,
                     GL_STATIC_DRAW)

        # Unbind buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)


    def mapTexture(self):
        img = Image.open(self.filepath + "Texture.jpg")
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
        glBindTexture(GL_TEXTURE_2D, 0)

        return textID