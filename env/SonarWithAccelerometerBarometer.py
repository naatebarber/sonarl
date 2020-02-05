import random
import math
import numpy as np

# ENV assumes automatic correction for rotational and y-plane acceleration via barometer and accelerometer sensors.

class SonarWithAcceleromenterBarometer:
    def __init__(self):
        self.bound = 1000
        self.velocity = np.zeros([3])
        self.position = np.random.randint(-self.bound, self.bound, [3])
        self.yaw_angle = 0

    def set_init_bound(self, bound):
        self.bound = bound
        return self

    def set_init_velocity(self, velocity):
        self.velocity = velocity
        return self

    def set_init_nonzero_yaw(self):
        self.yaw_angle = np.random.randint(0, 360)
        return self

    def ordi(self):
        pass

    def step(self, action):
        # Action => Motor set invoked to high speed => (Hover, Roll, Pitch, Yaw) => Shape = 4
        delta_hover = 0
        delta_roll = 0
        delta_pitch = 0
        delta_yaw = 0

        if action is 0:
            # HOVER: Alter Y-plane vector POS
            delta_hover = 4.9
        elif action is 1:
            # HOVER: Alter Y-plane vector NEG
            delta_hover = -4.9
        elif action is 2:
            # ROLL: Alter X-plane vector POS
            delta_roll = 5
        elif action is 3:
            #ROLL: Alter X-plane vector NEG
            delta_roll = -5
        elif action is 4:
            # PITCH: Alter Z-plane vector POS
            delta_pitch = 5
        elif action is 5:
            # PITCH: Alter Y-plane vector NEG
            delta_pitch = -5
        elif action is 6:
            # YAW: Alter Yaw-angle to shift future acceleration POS
            delta_yaw = 10
        elif action is 7:
            # YAW: Alter Yaw-angle to shift future acceleration NEG
            delta_yaw = -10

        # alter yaw angle
        self.yaw_angle += delta_yaw

        # alter velocity vector
        self.velocity[0] += math.cos(self.dtr(self.yaw_angle)) * delta_roll + math.cos(self.dtr(self.yaw_angle + 90)) * delta_pitch 
        self.velocity[1] += math.cos(self.dtr(self.yaw_angle + 90)) * delta_pitch + math.cos(self.dtr(self.yaw_angle)) * delta_roll
        self.velocity[2] += delta_hover

        # update position vector
        for i in range(len(self.velocity)): self.position[i] += self.velocity[i]

        # return ordi
        return self.ordi()

    def reset(self):
        self.position = np.random.randint(-self.bound, self.bound, [3])
        self.velocity = np.zeros([3])
        self.yaw_angle = 0
        return self.ordi()

    def dtr(deg):
        return deg * (math.pi / 180)
    
