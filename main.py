import pyrr

from glfw import *
from OpenGL.GL import *

import numpy as np
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
uniform mat4 light;

out vec2 v_texture;
out vec3 fragNormal;

void main()
{
    fragNormal = (light * vec4(a_normal, 0.0f)).xyz;
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

FRAGMENT_SRC = """
# version 330

in vec2 v_texture;
in vec3 fragNormal;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    vec3 ambientLightIntensity = vec3(0.3f, 0.2f, 0.4f);
    vec3 sunLightIntensity = vec3(0.9f, 0.9f, 0.9f);
    vec3 sunLightDirection = normalize(vec3(-5.0f, 5.0f, 5.0f));

    vec4 texel = texture(s_texture, v_texture);

    vec3 lightIntensity = ambientLightIntensity + sunLightIntensity * max(dot(fragNormal, sunLightDirection), 0.0f);

    out_color = vec4(texel.rgb * lightIntensity, texel.a);
}
"""


# glfw callback functions
def window_resize(window, width, height):
    glViewport(0, 0, width, height)

    # prevent division by zero error when minimising screen
    if height == 0:
        height = 1

    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

def mouse_look_clb(window, xpos, ypos):
    global lastX, lastY

    if not look_around:
        lastX = xpos
        lastY = ypos

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

def mouse_button_clb(window, button, action, mods):
    global look_around

    if button == MOUSE_BUTTON_RIGHT and action == PRESS:
        look_around = True
    else:
        look_around = False


def scroll_callback(window, xoff, yoff):
    global velocity

    if yoff == 1:
        velocity += 0.01
    if yoff == -1:
        velocity -= 0.01

def key_callback(window, key, scancode, action, mods):
    global left, right, forward, backward, up, down

    if key == KEY_ESCAPE and action == PRESS:
        set_window_should_close(window, True)

    if key == KEY_W and action == PRESS:
        forward = True
    elif key == KEY_W and action == RELEASE:
        forward = False

    if key == KEY_S and action == PRESS:
        backward = True
    elif key == KEY_S and action == RELEASE:
        backward = False

    if key == KEY_A and action == PRESS:
        left = True
    elif key == KEY_A and action == RELEASE:
        left = False

    if key == KEY_D and action == PRESS:
        right = True
    elif key == KEY_D and action == RELEASE:
        right = False

    if key == KEY_SPACE and action == PRESS:
        up = True
    elif key == KEY_SPACE and action == RELEASE:
        up = False

    if key == KEY_LEFT_CONTROL and action == PRESS:
        down = True
    elif key == KEY_LEFT_CONTROL and action == RELEASE:
        down = False

    # if key in [KEY_W, KEY_S, KEY_D, KEY_A] and action == RELEASE:
    #     left, right, forward, backward = False, False, False, False

def process_gamepad_input(gamepad_state):
    if gamepad_state == None:
        return

    global left, right, forward, backward, up, down

    # process right thumbstick to turn camera
    turn_multiplier = 5
    right_xoffset, right_yoffset = gamepad_state[1][2:4]
    cam.process_mouse_movement(right_xoffset * turn_multiplier, -right_yoffset * turn_multiplier)

    # process left thumbstick to move front/back, left/right
    left_xoffset, left_yoffset = gamepad_state[1][0:2]

    if abs(left_xoffset) > 0.2:
        if left_xoffset > 0:
            left = False
            right = True
        elif left_xoffset < 0:
            left = True
            right = False
    else:
        left = False
        right = False

    if abs(left_yoffset) > 0.2:
        if left_yoffset > 0:
            forward = False
            backward = True
        elif left_yoffset < 0:
            forward = True
            backward = False
    else:
        forward = False
        backward = False

    # process left/right triggers to move down/up
    left_trigger, right_trigger = gamepad_state[1][4:]

    if left_trigger == 1:
        down = True
    else:
        down = False

    if right_trigger == 1:
        up = True
    else:
        up = False


# move camera view, called in the main loop
def move_cam(velocity):
    if left:
        cam.process_keyboard("LEFT", velocity)
    if right:
        cam.process_keyboard("RIGHT", velocity)
    if forward:
        cam.process_keyboard("FORWARD", velocity)
    if backward:
        cam.process_keyboard("BACKWARD", velocity)
    if up:
        cam.process_keyboard("UP", velocity)
    if down:
        cam.process_keyboard("DOWN", velocity)


# Initializing glfw library
if not init():
    raise Exception("Error: glfw cannot be initialized")

# initialising camera
cam = Camera(boundary=pyrr.Vector3([100.0, 100.0, 100.0]))
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
look_around = False
left, right, forward, backward, up, down = [False for x in range(6)]
velocity = 0.05

# If we are planning to use anything above 2.1 we must at least
# request a 3.3 core context to make this work across platforms.
window_hint(CONTEXT_VERSION_MAJOR, 4)
window_hint(CONTEXT_VERSION_MINOR, 1)
window_hint(OPENGL_PROFILE, OPENGL_CORE_PROFILE)
window_hint(OPENGL_FORWARD_COMPAT, GL_TRUE)

# 4 MSAA is a good default with wide support
window_hint(SAMPLES, 4)

# Creating the window
window = create_window(WIDTH, HEIGHT, NAME, None, None)
print("Window initialised!")

# Check if window was created
if not window:
    terminate()
    raise Exception("Error: glfw window cannot be created")

# Query the actual framebuffer size so we can set the right viewport later
# -> glViewport(0, 0, framebuffer_size[0], framebuffer_size[1])
framebuffer_size = get_framebuffer_size(window)

# Set window's position
set_window_pos(window, 400, 200)

# Set the callback function for window resize
set_window_size_callback(window, window_resize)

# set mouse position callback
set_cursor_pos_callback(window, mouse_look_clb)

# set mouse button callback
set_mouse_button_callback(window, mouse_button_clb)

# set mouse scroll callback
set_scroll_callback(window, scroll_callback)

# set keyboard input callback
set_key_callback(window, key_callback)


# Load 3d meshes
planet_names = ['moon', 'sun', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
planet_indices = [None for i in range(len(planet_names))]
planet_buffers = [None for i in range(len(planet_names))]

for index in range(len(planet_names)):
    planet_indices[index], planet_buffers[index] = ObjLoader.load_model(f'data/{planet_names[index]}/Model.obj')

print("Meshes loaded!")

# set each planet's rotation speed
planet1_speed = [0.1, 0.1, 0.07, 0.02, 0.09, 0.08, 0.2, 0.15, 0.095, 0.1] #planet rotation
planet_speed = [0.4, 0, 0.6, 0.5, 0.4, 0.35, 0.1, 0.2, 0.15, 0.1] #planet oribit

# set each planet's size
planet_scaling = [0.1, 1.4, 0.3, 0.5, 0.7, 0.5, 0.9, 0.8, 0.7, 0.4]


# Make the context current
make_context_current(window)

VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

shader = compileProgram(
    compileShader(VERTEX_SRC, GL_VERTEX_SHADER),
    compileShader(FRAGMENT_SRC, GL_FRAGMENT_SHADER)
)

# VAO, VBO and EBO binding
VAO = glGenVertexArrays(10)
VBO = glGenBuffers(10)
#EBO = glGenBuffers(10)


def configure_arrays(index):
    # VAO
    glBindVertexArray(VAO[index])

    # VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, planet_buffers[index].nbytes, planet_buffers[index], GL_STATIC_DRAW)

    # EBO
    #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[index])
    #glBufferData(GL_ELEMENT_ARRAY_BUFFER, planet_indices[index].nbytes, planet_indices[index], GL_STATIC_DRAW)

    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, planet_buffers[index].itemsize * 8, ctypes.c_void_p(0))

    # textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, planet_buffers[index].itemsize * 8, ctypes.c_void_p(12))

    # normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, planet_buffers[index].itemsize * 8, ctypes.c_void_p(20))
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

projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)


moon_coor = [50, 1, -50]
sun_coor = [0, 0, 0]
mercury_coor = [10, 0, -10]
venus_coor = [12, 0, -12]
earth_coor = [12, 0, -12]
mars_coor = [20, 0, -20]
jupiter_coor = [18, 0, -18]
saturn_coor = [24, 0, -24]
uranus_coor = [40, 0, -40]
neptune_coor = [65, 0, -65]

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
light_loc = glGetUniformLocation(shader, "light")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


def rotate_draw(index):
    # Rotate
    #rot_x = pyrr.Matrix44.from_x_rotation(planet_speed[index] * get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(planet_speed[index] * get_time())
    #rot = pyrr.matrix44.multiply(rot_y, rot_x)
    rot1_y = pyrr.Matrix44.from_y_rotation(planet1_speed[index] * get_time()) 
    
    scale = pyrr.Matrix44.from_scale(pyrr.Vector3([planet_scaling[index] for x in range(3)]))
    rotate = pyrr.matrix44.multiply(rot1_y, scale) #rotate
    final = pyrr.matrix44.multiply(planet_positions[index], rotate) #translate
    model = pyrr.matrix44.multiply(final, rot_y) #rotate
    


    # Draw
    glBindVertexArray(VAO[index])
    glBindTexture(GL_TEXTURE_2D, textures[index])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glUniformMatrix4fv(light_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(planet_indices[index]))
    # glDrawElements(GL_TRIANGLES, len(planet_indices[index]), GL_UNSIGNED_INT, None)


# The main application loop
while not window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    for index in range(len(planet_names)):
        rotate_draw(index)

    # Swap front and back buffers
    swap_buffers(window)

    # Poll for and process events
    poll_events()

    process_gamepad_input(get_gamepad_state(0))

    move_cam(velocity)

# terminate glfw, free up allocated resources
terminate()
