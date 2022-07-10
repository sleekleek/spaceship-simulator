import glfw, pyrr, pygame

from OpenGL.GL import *
from pygame.locals import *

from camera import Camera
from objLoader import ObjLoader
from textureMapper import TextureMapper
from OpenGL.GL.shaders import compileProgram, compileShader


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
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

def mouse_enter_clb(window, entered):
    global first_mouse

    if entered:
        first_mouse = False
    else:
        first_mouse = True

def mouse_look_clb(window, xpos, ypos):
    global lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

def key_callback(window, key, scancode, action, mods):
    global left, right, forward, backward

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False
    # if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A] and action == glfw.RELEASE:
    #     left, right, forward, backward = False, False, False, False

# move camera view, called in the main loop
def move_cam():
    if left:
        cam.process_keyboard("LEFT", 0.05)
    if right:
        cam.process_keyboard("RIGHT", 0.05)
    if forward:
        cam.process_keyboard("FORWARD", 0.05)
    if backward:
        cam.process_keyboard("BACKWARD", 0.05)


# Initializing glfw library
if not glfw.init():
    raise Exception("Error: glfw cannot be initialized")

# initialising camera
cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward = False, False, False, False

# Creating the window
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
window = glfw.create_window(WIDTH, HEIGHT, NAME, None, None)
print("Window initialised!")

# Check if window was created
if not window:
    glfw.terminate()
    raise Exception("Error: glfw window cannot be created")

# Set window's position
glfw.set_window_pos(window, 200, 200)

# Set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# set mouse entering window callback
glfw.set_cursor_enter_callback(window, mouse_enter_clb)

# set mouse position callback
glfw.set_cursor_pos_callback(window, mouse_look_clb)

# set keyboard input callback
glfw.set_key_callback(window, key_callback)


# Make the context current
glfw.make_context_current(window)
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

# Load 3d meshes
planet_names = ['moon', 'sun', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
planet_indices = [None for i in range(len(planet_names))]
planet_buffers = [None for i in range(len(planet_names))]

for index in range(len(planet_names)):
    planet_indices[index], planet_buffers[index] = ObjLoader.load_model(f'data/{planet_names[index]}/Model.obj')

print("Meshes loaded!")

shader = OpenGL.GL.shaders.compileProgram(compileShader(
    VERTEX_SRC, GL_VERTEX_SHADER), compileShader(FRAGMENT_SRC, GL_FRAGMENT_SHADER))

# VAO, VBO and EBO binding
VAO = glGenVertexArrays(10)
VBO = glGenBuffers(10)
# EBO = glGenBuffers(10)


def configure_arrays(index):
    # VAO
    glBindVertexArray(VAO[index])

    # VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, planet_buffers[index].nbytes, planet_buffers[index], GL_STATIC_DRAW)

    # EBO
    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[index])
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, planet_indices[index].nbytes, planet_indices[index], GL_STATIC_DRAW)

    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, planet_buffers[index].itemsize * 8, ctypes.c_void_p(0))

    # textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, planet_buffers[index].itemsize * 8, ctypes.c_void_p(12))

    # normals
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, planet_buffers[index].itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)


for index in range(len(planet_names)):
    configure_arrays(index)

print("VAO, VBO binded!")

# Map textures
textures = glGenTextures(10)

for index in range(len(planet_names)):
    TextureMapper(f'data/{planet_names[index]}/Texture.jpg', textures[index])

print("Textures mapped!")

glUseProgram(shader)
#glClearColor(0, 0, 0, 1)    # Background colour
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)

# Set positions
moon_coor = [0, 8, -12]
sun_coor = [-20, 0, 0]
mercury_coor = [-15, 0, 0]
venus_coor = [-10, 0, 0]
earth_coor = [-5, 0, 0]
mars_coor = [0, 0, 0]
jupiter_coor = [5, 0, 0]
saturn_coor = [10, 0, 0]
uranus_coor = [15, 0, 0]
neptune_coor = [20, 0, 0]

planet_translations = [moon_coor, sun_coor, mercury_coor, venus_coor, earth_coor, mars_coor, jupiter_coor, saturn_coor, uranus_coor, neptune_coor]
planet_positions = []

for index in range(len(planet_names)):
    planet_positions.append(pyrr.matrix44.create_from_translation(pyrr.Vector3(planet_translations[index])))

# Eye, target, up
view = pyrr.matrix44.create_look_at(pyrr.Vector3(
    [0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


def rotate_draw(index):
    # Rotate
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, planet_positions[index])

    # Draw
    glBindVertexArray(VAO[index])
    glBindTexture(GL_TEXTURE_2D, textures[index])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(planet_indices[index]))
    # glDrawElements(GL_TRIANGLES, len(planet_indices[index]), GL_UNSIGNED_INT, None)


# The main application loop
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    for index in range(len(planet_names)):
        rotate_draw(index)

    # Swap front and back buffers
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()

    move_cam()

# terminate glfw, free up allocated resources
glfw.terminate()
