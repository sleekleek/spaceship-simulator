import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

from objLoader import ObjLoader
from textureMapper import TextureMapper


NAME = 'Fly Me To The Moon'

VERTEX_SRC = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

FRAGMENT_SRC = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""


# glfw callback functions
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(
        45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# Initializing glfw library
if not glfw.init():
    raise Exception("Error: glfw cannot be initialized")

# Creating the window
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
window = glfw.create_window(1280, 720, NAME, None, None)
print("Window initialised!")

# Check if window was created
if not window:
    glfw.terminate()
    raise Exception("Error: glfw window cannot be created")

# Set window's position
glfw.set_window_pos(window, 200, 200)
# Set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)
# Make the context current
glfw.make_context_current(window)
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

# Load 3d meshes
planet_names = ['moon', 'sun', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
indices = [None for i in range(len(planet_names))]
buffers = [None for i in range(len(planet_names))]

for planet_index in range(len(planet_names)):
    indices[planet_index], buffers[planet_index] = ObjLoader.load_model(f'data/{planet_names[planet_index]}/Model.obj')

print("Meshes loaded!")

shader = OpenGL.GL.shaders.compileProgram(compileShader(
    VERTEX_SRC, GL_VERTEX_SHADER), compileShader(FRAGMENT_SRC, GL_FRAGMENT_SHADER))

# VAO, VBO and EBO binding
VAO = glGenVertexArrays(10)
VBO = glGenBuffers(10)
# EBO = glGenBuffers(10)

def configure_arrays(planet_index):
    # VAO
    glBindVertexArray(VAO[planet_index])
    # VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, buffers[planet_index].nbytes, buffers[planet_index], GL_STATIC_DRAW)
    # EBO
    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[planet_index])
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices[planet_index].nbytes, indices[planet_index], GL_STATIC_DRAW)
    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                          buffers[planet_index].itemsize * 8, ctypes.c_void_p(0))
    # textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                          buffers[planet_index].itemsize * 8, ctypes.c_void_p(12))
    # normals
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                          buffers[planet_index].itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)


for planet_index in range(len(planet_names)):
    configure_arrays(planet_index)

print("VAO, VBO binded!")

# Map textures
textures = glGenTextures(10)

for planet_index in range(len(planet_names)):
    TextureMapper(f'data/{planet_names[planet_index]}/Texture.jpg', textures[planet_index])

print("Textures mapped!")

glUseProgram(shader)
#glClearColor(0, 0, 0, 1)    # Background colour
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(
    45, 1280 / 720, 0.1, 100)

# Set positions
moon_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 8, -12]))
sun_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-20, 0, 0]))
mercury_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-15, 0, 0]))
venus_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-10, 0, 0]))
earth_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-5, 0, 0]))
mars_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
jupiter_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([5, 0, 0]))
saturn_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([10, 0, 0]))
uranus_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([15, 0, 0]))
neptune_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([20, 0, 0]))

positions = [moon_pos, sun_pos, mercury_pos, venus_pos, earth_pos, mars_pos, jupiter_pos, saturn_pos, uranus_pos, neptune_pos]

# Eye, target, up
view = pyrr.matrix44.create_look_at(pyrr.Vector3(
    [0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

# The main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def rotate_draw(planet_index):      
        # Rotate
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        model = pyrr.matrix44.multiply(rot_y, positions[planet_index])

        # Draw
        glBindVertexArray(VAO[planet_index])
        glBindTexture(GL_TEXTURE_2D, textures[planet_index])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(indices[planet_index]))
        # glDrawElements(GL_TRIANGLES, len(indices[planet_index]), GL_UNSIGNED_INT, None)

    for planet_index in range(len(planet_names)):
        rotate_draw(planet_index)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()
