import pyrr

from glfw import *
from OpenGL.GL import *

from camera import Camera
from pyexpat import model
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

out vec3 vposition;
out vec2 v_texture;
out vec3 fragNormal;

void main() {
    v_texture = a_texture;
    vposition = a_position;
    fragNormal = a_normal;
    gl_Position = projection * view * model * vec4(a_position, 1.0);
}
"""

FRAGMENT_SRC = """
# version 330

uniform mat4 model;
uniform sampler2D s_texture;

in vec2 v_texture;
in vec3 fragNormal;
in vec3 vposition;

out vec4 out_color;

void main() {
    vec3 gLightIntensities = vec3(5.0f, 5.0f, 5.0f);
    vec3 gLightPosition = vec3(0.0f, 0.0f, 0.0f);

    mat3 normalMatrix = transpose(inverse(mat3(model)));
    vec3 normal = normalize(normalMatrix * fragNormal);

    vec3 fragPosition = vec3(model * vec4(vposition, 1));

    vec3 surfaceToLight = gLightPosition - fragPosition;

    float brightness = dot(normal, surfaceToLight) / (length(surfaceToLight) * length(normal));
    brightness = clamp(brightness, 0.2, 1);

    vec4 surfaceColor = texture(s_texture, v_texture);
    out_color = vec4(brightness *  gLightIntensities * surfaceColor.rgb, surfaceColor.a);
}
"""


# glfw callback functions
def window_resize(window, width, height):
    glViewport(0, 0, width, height)

    # prevent division by zero error when minimising screen
    if height == 0:
        height = 1

    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, MAX_VISIBLE_DISTANCE)
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

    # Toggle look_around on right mouse button
    if (button == MOUSE_BUTTON_LEFT or button == MOUSE_BUTTON_RIGHT) and action == PRESS:
        look_around = True
    else:
        look_around = False

def scroll_callback(window, xoff, yoff):
    global velocity

    if yoff == 1 and velocity < 2 * scaling_multiplier:
        velocity *= 1.25
    elif yoff == -1 and velocity > 10:
        velocity /= 1.25

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

    if (key == KEY_LEFT_CONTROL or key == KEY_C) and action == PRESS:
        down = True
    elif (key == KEY_LEFT_CONTROL or key == KEY_C) and action == RELEASE:
        down = False

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


# move camera view and rotate spaceship, called in the main loop
def move_cam(velocity):
    plane_rotate_fb = 2.8
    plane_rotate_lr = 0

    if left:
        cam.process_keyboard("LEFT", velocity)
        plane_rotate_lr = 1
    if right:
        cam.process_keyboard("RIGHT", velocity)
        plane_rotate_lr = -1
    if forward:
        cam.process_keyboard("FORWARD", velocity)
        plane_rotate_fb = 3
    if backward:
        cam.process_keyboard("BACKWARD", velocity)
        plane_rotate_fb = 2.6
    if up:
        cam.process_keyboard("UP", velocity)
    if down:
        cam.process_keyboard("DOWN", velocity)

    return plane_rotate_fb, plane_rotate_lr


# Initializing glfw library
if not init():
    raise Exception("Error: glfw cannot be initialized")

# initialising camera
cam = Camera(boundary=pyrr.Vector3([100.0, 100.0, 100.0]))
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2

look_around = False
left, right, forward, backward, up, down = [False for x in range(6)]

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

# Make the context current
make_context_current(window)
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)


# Spaceship
# load plane mesh
obj = ObjLoader()
spaceship_indices, spaceship_buffer = obj.load_model("data/spaceship/spaceship.obj")
print("Spaceship mesh loaded!")

# spaceship VAO binding
spaceship_VAO = glGenVertexArrays(1)
spaceship_VBO = glGenBuffers(1)

glBindVertexArray(spaceship_VAO)
glBindBuffer(GL_ARRAY_BUFFER, spaceship_VBO)
glBufferData(GL_ARRAY_BUFFER, spaceship_buffer.nbytes, spaceship_buffer, GL_STATIC_DRAW)

# spaceship vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, spaceship_buffer.itemsize * 8, ctypes.c_void_p(0))
# spaceship textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, spaceship_buffer.itemsize * 8, ctypes.c_void_p(12))
# spaceship normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, spaceship_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

print("Spaceship VAO, VBO binded!")

# spaceship texture load
spaceship_texturemap = "data/spaceship/spaceship_black.jpeg" 
spaceship_texture = glGenTextures(1)

TextureMapper(spaceship_texturemap, spaceship_texture)
print("Spaceship textures mapped!")


# Planets
# Load 3d meshes
planet_names = ['moon', 'sun', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
planet_indices = [None for i in range(len(planet_names))]
planet_buffers = [None for i in range(len(planet_names))]

for index in range(len(planet_names)):
    obj = ObjLoader()
    planet_indices[index], planet_buffers[index] = obj.load_model(f'data/{planet_names[index]}/Model.obj')

print("Planet meshes loaded!")

# set each planet's rotation speed
#                  moon    sun  mercury venus  earth   mars jupiter saturn uranus neptune
planet_rotation = [0.034, 0.037, 0.006, 0.009, 1.000, 0.971, 2.415, 2.252, 1.393, 1.490]  # planet rotation around its own axis

orbit_speed_multiplier = 0.5
planet_orbit    = [1.003, 0.000, 1.590, 1.180, 1.000, 0.808, 0.439, 0.325, 0.228, 0.182]  # planet orbit around the origin (SUN)
planet_orbit = [planet * orbit_speed_multiplier for planet in planet_orbit]

scaling_multiplier = 500
planet_scaling  = [0.272, 7.00, 0.7, 0.949, 1.000, 0.532, 7.21, 5.450, 4.010, 3.880]  # planet size
planet_scaling = [planet * scaling_multiplier for planet in planet_scaling]

earth_distance = 75 * scaling_multiplier
planet_distance = [1.105, 0.000, 0.870, 0.950, 1.100, 1.350, 2.000, 3.000, 5.17, 7.18]  # ratio of distances from the sun
planet_distance = [planet * earth_distance for planet in planet_distance]

planet_positions = []

for index in range(len(planet_names)):
    planet_positions.append(
        pyrr.matrix44.create_from_translation(
            pyrr.Vector3(
                [planet_distance[index], 0, 0]
            )
        )
    )

velocity = 0.2 * scaling_multiplier
MAX_VISIBLE_DISTANCE = 10 * earth_distance

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
    glBindBuffer(GL_ARRAY_BUFFER, VBO[index])
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

print("Planet VAO, VBO binded!")


# Map textures
textures = glGenTextures(10)

for index in range(len(planet_names)):
    TextureMapper(f'data/{planet_names[index]}/Texture.jpg', textures[index])

print("Planet textures mapped!")



#glClearColor(0, 0, 0, 1)    # Background colour

glUseProgram(shader);

glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


# spaceship_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))
projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, MAX_VISIBLE_DISTANCE)
# Eye, target, up
view = pyrr.matrix44.create_look_at(
    pyrr.Vector3([0, 0, 8]),
    pyrr.Vector3([0, 0, 0]),
    pyrr.Vector3([0, 1, 0])
)

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")
light_loc = glGetUniformLocation(shader, "light")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


def rotate_draw(index):
    # Rotate
    rot_orbit = pyrr.Matrix44.from_y_rotation(planet_orbit[index] * get_time())
    rot_rotation = pyrr.Matrix44.from_y_rotation(planet_rotation[index] * get_time()) 
    
    scale = pyrr.Matrix44.from_scale(pyrr.Vector3([planet_scaling[index] for x in range(3)]))
    translation = pyrr.matrix44.multiply(scale, planet_positions[index]) #translate to different positions
    rotate = pyrr.Matrix44(translation) * rot_rotation #rotate around its own axis
    model = pyrr.matrix44.multiply(rotate, rot_orbit) #orbit around the sun
    
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

    process_gamepad_input(get_gamepad_state(0))

    plane_rotate_fb, plane_rotate_lr = move_cam(velocity)

    for index in range(len(planet_names)):
        rotate_draw(index)
        
    # draw spaceship
    plane_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -2, -9]))
    scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))  
    rotate_x = pyrr.matrix44.create_from_x_rotation(plane_rotate_fb)  
    rotate_y = pyrr.matrix44.create_from_y_rotation(0.08 * plane_rotate_lr)
    rotate_z = pyrr.matrix44.create_from_z_rotation(0.08 * plane_rotate_lr)

    identity_mat = pyrr.matrix44.create_identity()
    pos = pyrr.matrix44.multiply(plane_pos, identity_mat) 
    pos = pyrr.matrix44.multiply(rotate_x, pos) 
    pos = pyrr.matrix44.multiply(rotate_y, pos) 
    pos = pyrr.matrix44.multiply(rotate_z, pos) 
    pos = pyrr.matrix44.multiply(scale, pos) 

    glBindVertexArray(spaceship_VAO)
    glBindTexture(GL_TEXTURE_2D, spaceship_texture)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, identity_mat)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pos)
    glDrawArrays(GL_TRIANGLES, 0, len(spaceship_indices))

    # Swap front and back buffers
    swap_buffers(window)

    # Poll for and process events
    poll_events()

    process_gamepad_input(get_gamepad_state(0))


# terminate glfw, free up allocated resources
terminate()
