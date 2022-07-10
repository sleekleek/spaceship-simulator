from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians, pow
import numpy as np

# https://github.com/totex/Learn-OpenGL-in-python/blob/master/camera.py

np.seterr(divide='ignore', invalid='ignore')

class Camera:
    def __init__(self, boundary):
        self.boundary = boundary
        
        self.camera_pos = Vector3([0.0, 0.0, 0.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.25
        self.jaw = -90
        self.pitch = 0

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)
    
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45:
                self.pitch = 45
            if self.pitch < -45:
                self.pitch = -45

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(
            self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(
            vector3.cross(self.camera_right, self.camera_front))

    def check_new_camera_pos(self, new_camera_pos):
        # Check if new_camera_pos is within ellipsoid
        if pow(new_camera_pos.x / self.boundary.x, 2) + pow(new_camera_pos.y / self.boundary.y, 2) + pow(new_camera_pos.z / self.boundary.z, 2) < 1:
            return True 
        else:
            return False

    # Camera method for the WASD movement
    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            new_camera_pos = self.camera_pos + self.camera_front * velocity
        if direction == "BACKWARD":
            new_camera_pos = self.camera_pos - self.camera_front * velocity
        if direction == "LEFT":
            new_camera_pos = self.camera_pos - self.camera_right * velocity
        if direction == "RIGHT":
            new_camera_pos = self.camera_pos + self.camera_right * velocity
        
        if (self.check_new_camera_pos(new_camera_pos)):
                self.camera_pos = new_camera_pos