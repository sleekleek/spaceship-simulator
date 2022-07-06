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

# Load 3d meshes
moon_indices, moon_buffer = ObjLoader.load_model("data/moon/Model.obj")
sun_indices, sun_buffer = ObjLoader.load_model("data/sun/Model.obj")
mercury_indices, mercury_buffer = ObjLoader.load_model("data/mercury/Model.obj")
venus_indices, venus_buffer = ObjLoader.load_model("data/venus/Model.obj")
earth_indices, earth_buffer = ObjLoader.load_model("data/earth/Model.obj")
mars_indices, mars_buffer = ObjLoader.load_model("data/mars/Model.obj")
jupiter_indices, jupiter_buffer = ObjLoader.load_model("data/jupiter/Model.obj")
saturn_indices, saturn_buffer = ObjLoader.load_model("data/saturn/Model.obj")
uranus_indices, uranus_buffer = ObjLoader.load_model("data/uranus/Model.obj")
neptune_indices, neptune_buffer = ObjLoader.load_model("data/neptune/Model.obj")
print("Meshes loaded!")

shader = compileProgram(compileShader(
    VERTEX_SRC, GL_VERTEX_SHADER), compileShader(FRAGMENT_SRC, GL_FRAGMENT_SHADER))

# VAO, VBO and EBO binding
VAO = glGenVertexArrays(10)
VBO = glGenBuffers(10)
# EBO = glGenBuffers(10)

# Moon VAO
glBindVertexArray(VAO[0])
# Moon VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, moon_buffer.nbytes, moon_buffer, GL_STATIC_DRAW)
# Moon EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[0])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, moon_indices.nbytes, moon_indices, GL_STATIC_DRAW)
# Moon vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      moon_buffer.itemsize * 8, ctypes.c_void_p(0))
# Moon textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      moon_buffer.itemsize * 8, ctypes.c_void_p(12))
# Moon normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      moon_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# Sun VAO
glBindVertexArray(VAO[1])
# Sun VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, sun_buffer.nbytes, sun_buffer, GL_STATIC_DRAW)
# Sun EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[1])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, sun_indices.nbytes, sun_indices, GL_STATIC_DRAW)
# Sun vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      sun_buffer.itemsize * 8, ctypes.c_void_p(0))
# Sun textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      sun_buffer.itemsize * 8, ctypes.c_void_p(12))
# Sun normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      sun_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# Mercury VAO
glBindVertexArray(VAO[2])
# Mercury VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, mercury_buffer.nbytes,
             mercury_buffer, GL_STATIC_DRAW)
# Mercury EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[2])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, mercury_indices.nbytes, mercury_indices, GL_STATIC_DRAW)
# Mercury vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      mercury_buffer.itemsize * 8, ctypes.c_void_p(0))
# Mercury textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      mercury_buffer.itemsize * 8, ctypes.c_void_p(12))
# Mercury normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      mercury_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# Venus VAO
glBindVertexArray(VAO[3])
# Venus VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
glBufferData(GL_ARRAY_BUFFER, venus_buffer.nbytes,
             venus_buffer, GL_STATIC_DRAW)
# Venus EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[3])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, venus_indices.nbytes, venus_indices, GL_STATIC_DRAW)
# Venus vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      venus_buffer.itemsize * 8, ctypes.c_void_p(0))
# Venus textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      venus_buffer.itemsize * 8, ctypes.c_void_p(12))
# Venus normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      venus_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# Earth VAO
glBindVertexArray(VAO[4])
# Earth VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[4])
glBufferData(GL_ARRAY_BUFFER, earth_buffer.nbytes,
             earth_buffer, GL_STATIC_DRAW)
# Earth EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[4])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, earth_indices.nbytes, earth_indices, GL_STATIC_DRAW)
# Earth vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      earth_buffer.itemsize * 8, ctypes.c_void_p(0))
# Earth textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      earth_buffer.itemsize * 8, ctypes.c_void_p(12))
# Earth normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      earth_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# Mars VAO
glBindVertexArray(VAO[5])
# Mars VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[5])
glBufferData(GL_ARRAY_BUFFER, mars_buffer.nbytes, mars_buffer, GL_STATIC_DRAW)
# Mars EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[5])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, mars_indices.nbytes, mars_indices, GL_STATIC_DRAW)
# Mars vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      mars_buffer.itemsize * 8, ctypes.c_void_p(0))
# Mars textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      mars_buffer.itemsize * 8, ctypes.c_void_p(12))
# Mars normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      mars_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# Jupiter VAO
glBindVertexArray(VAO[6])
# Jupiter VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[6])
glBufferData(GL_ARRAY_BUFFER, jupiter_buffer.nbytes,
             jupiter_buffer, GL_STATIC_DRAW)
# Jupiter EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[6])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, jupiter_indices.nbytes, jupiter_indices, GL_STATIC_DRAW)
# Jupiter vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      jupiter_buffer.itemsize * 8, ctypes.c_void_p(0))
# Jupiter textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      jupiter_buffer.itemsize * 8, ctypes.c_void_p(12))
# Jupiter normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      jupiter_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# Saturn VAO
glBindVertexArray(VAO[7])
# Saturn VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[7])
glBufferData(GL_ARRAY_BUFFER, saturn_buffer.nbytes,
             saturn_buffer, GL_STATIC_DRAW)
# Saturn EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[7])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, saturn_indices.nbytes, saturn_indices, GL_STATIC_DRAW)
# Saturn vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      saturn_buffer.itemsize * 8, ctypes.c_void_p(0))
# Saturn textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      saturn_buffer.itemsize * 8, ctypes.c_void_p(12))
# Saturn normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      saturn_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# Uranus VAO
glBindVertexArray(VAO[8])
# Uranus VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[8])
glBufferData(GL_ARRAY_BUFFER, uranus_buffer.nbytes,
             uranus_buffer, GL_STATIC_DRAW)
# Uranus EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[8])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, uranus_indices.nbytes, uranus_indices, GL_STATIC_DRAW)
# Uranus vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      uranus_buffer.itemsize * 8, ctypes.c_void_p(0))
# Uranus textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      uranus_buffer.itemsize * 8, ctypes.c_void_p(12))
# Uranus normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      uranus_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# Neptune VAO
glBindVertexArray(VAO[9])
# Neptune VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[9])
glBufferData(GL_ARRAY_BUFFER, neptune_buffer.nbytes,
             neptune_buffer, GL_STATIC_DRAW)
# Neptune EBO
# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[9])
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, neptune_indices.nbytes, neptune_indices, GL_STATIC_DRAW)
# Neptune vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      neptune_buffer.itemsize * 8, ctypes.c_void_p(0))
# Neptune textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      neptune_buffer.itemsize * 8, ctypes.c_void_p(12))
# Neptune normals
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      neptune_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

print("VAO, VBO binded!")

# Map textures
textures = glGenTextures(10)
TextureMapper("data/moon/Texture.jpg", textures[0])
TextureMapper("data/sun/Texture.jpg", textures[1])
TextureMapper("data/mercury/Texture.jpg", textures[2])
TextureMapper("data/venus/Texture.jpg", textures[3])
TextureMapper("data/earth/Texture.jpg", textures[4])
TextureMapper("data/mars/Texture.jpg", textures[5])
TextureMapper("data/jupiter/Texture.jpg", textures[6])
TextureMapper("data/saturn/Texture.jpg", textures[7])
TextureMapper("data/uranus/Texture.jpg", textures[8])
TextureMapper("data/neptune/Texture.jpg", textures[9])
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

    # Rotate moon
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, moon_pos)
    # Draw moon
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(moon_indices))
    # glDrawElements(GL_TRIANGLES, len(moon_indices), GL_UNSIGNED_INT, None)

    # Rotate sun
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, sun_pos)
    # Draw sun
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(sun_indices))
    # glDrawElements(GL_TRIANGLES, len(sun_indices), GL_UNSIGNED_INT, None)

    # Rotate mercury
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, mercury_pos)
    # Draw mercury
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(mercury_indices))
    # glDrawElements(GL_TRIANGLES, len(mercury_indices), GL_UNSIGNED_INT, None)

    # Rotate venus
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, venus_pos)
    # Draw venus
    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(venus_indices))
    # glDrawElements(GL_TRIANGLES, len(venus_indices), GL_UNSIGNED_INT, None)

    # Rotate earth
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, earth_pos)
    # Draw earth
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(earth_indices))
    # glDrawElements(GL_TRIANGLES, len(earth_indices), GL_UNSIGNED_INT, None)

    # Rotate mars
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, mars_pos)
    # Draw mars
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(mars_indices))
    # glDrawElements(GL_TRIANGLES, len(mars_indices), GL_UNSIGNED_INT, None)

    # Rotate jupiter
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, jupiter_pos)
    # Draw jupiter
    glBindVertexArray(VAO[6])
    glBindTexture(GL_TEXTURE_2D, textures[6])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(jupiter_indices))
    # glDrawElements(GL_TRIANGLES, len(jupiter_indices), GL_UNSIGNED_INT, None)

    # Rotate saturn
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, saturn_pos)
    # Draw saturn
    glBindVertexArray(VAO[7])
    glBindTexture(GL_TEXTURE_2D, textures[7])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(saturn_indices))
    # glDrawElements(GL_TRIANGLES, len(saturn_indices), GL_UNSIGNED_INT, None)

    # Rotate uranus
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, uranus_pos)
    # Draw uranus
    glBindVertexArray(VAO[8])
    glBindTexture(GL_TEXTURE_2D, textures[8])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(uranus_indices))
    # glDrawElements(GL_TRIANGLES, len(uranus_indices), GL_UNSIGNED_INT, None)

    # Rotate neptune
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, neptune_pos)
    # Draw neptune
    glBindVertexArray(VAO[9])
    glBindTexture(GL_TEXTURE_2D, textures[9])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(neptune_indices))
    # glDrawElements(GL_TRIANGLES, len(neptune_indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()