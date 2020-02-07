import random
import math
import numpy as np

# ENV assumes automatic correction for rotational and y-plane acceleration via barometer and accelerometer sensors.

class SonarWithAccelerometerBarometer:
    def __init__(self):
        self.bound = 1000
        self.padding = 200
        self.velocity = np.zeros([3])
        self.position = np.random.randint(-(self.bound - self.padding), self.bound - self.padding, [3])
        self.yaw_angle = 0
        # env info
        self.num_actions = 9
        self.num_states = 6

    def set_init_bound(self, bound):
        self.bound = bound
        return self

    def set_init_padding(self, padding):
        self.padding = padding
        return self

    def set_init_velocity(self, velocity):
        self.velocity = velocity
        return self

    def set_init_nonzero_yaw(self):
        self.yaw_angle = np.random.randint(0, 360)
        return self

    def ordi(self):
        # calculate sonar top/bottom (independent of yaw)
        sonar_top = self.bound - self.position[2]
        sonar_bottom = self.bound * 2 - sonar_top

        '''
        calculate sonar that changes as a result of yaw
        find hypotenuse to be = distance_from_face_n / cosine(degrees_yaw)

                    z face 0
                    - - - - 
                   |       | 
         x face 0  |  x z  |  x face 1
                   |       |
                    - - - - 
                    z face 2

        position vector is type [x, z, y]
        '''

        # trig adjacents
        distance_x_0 = abs(self.bound - self.position[0])
        distance_x_1 = abs((2 * self.bound) - distance_x_0)
        distance_z_0 = abs(self.bound - self.position[1])
        distance_z_1 = abs((2 * self.bound) - distance_z_0)

        # assuming no yaw:
        # sonar front
        sonar_0 = distance_z_0 / abs(math.cos(self.yaw_angle))
        sonar_1 = distance_z_1 / abs(math.cos(self.yaw_angle))
        sonar_2 = distance_x_0 / abs(math.cos(self.yaw_angle + 90))
        sonar_3 = distance_x_1 / abs(math.cos(self.yaw_angle + 90))
        
        # reassign for yaw
        # return sonar shape = [front, back, left, right, top, bottom]
        sonar = None

        if self.yaw_angle > 315 or self.yaw_angle <= 45:
            sonar = [sonar_0, sonar_1, sonar_2, sonar_3, sonar_top, sonar_bottom]
        elif self.yaw_angle <= 135:
            sonar = [sonar_2, sonar_3, sonar_1, sonar_0, sonar_top, sonar_bottom]
        elif self.yaw_angle <= 225:
            sonar = [sonar_1, sonar_0, sonar_3, sonar_2, sonar_top, sonar_bottom]
        elif self.yaw_angle <= 315:
            sonar = [sonar_3, sonar_2, sonar_0, sonar_1, sonar_top, sonar_bottom]
        # observation is 6 sonar inputs for each 'face' of the agent drone
        observation = sonar

        # find resultant distance vector from center
        x_dist = abs(self.position[0])
        z_dist = abs(self.position[1])
        y_dist = abs(self.position[2])
        xz_dist = math.sqrt(math.pow(x_dist, 2) + math.pow(z_dist, 2))
        xyz_dist = math.sqrt(math.pow(xz_dist, 2) + math.pow(y_dist, 2))
        max_reward = 10
        # corner of cube = max travel distance before episode reset
        max_travel_distance = math.sqrt(2 * math.pow(self.bound, 2))
        reward_multiplier = math.pow((1 - xyz_dist / max_travel_distance), 2)
        # reward is maximized as the agent approaches the center of the map
        reward = reward_multiplier * max_reward

        # done if agent exceeds boundary on any plane
        print(self.position, self.velocity)
        done = True if (x_dist > self.bound or y_dist > self.bound or z_dist > self.bound) else False

        return [[float(o) for o in observation], float(reward), done]
        

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
            # PITCH: Alter X-plane vector NEG
            delta_pitch = -5
        elif action is 6:
            # YAW: Alter Yaw-angle to shift future acceleration POS
            delta_yaw = 10
        elif action is 7:
            # YAW: Alter Yaw-angle to shift future acceleration NEG
            delta_yaw = -10

        # alter yaw angle
        self.yaw_angle += delta_yaw
        self.yaw_angle = self.yaw_angle % 360

        print("YAW: {}".format(self.yaw_angle))

        # alter velocity vector
        delta_vx = math.cos(self.dtr(self.yaw_angle)) * delta_roll + math.cos(self.dtr(self.yaw_angle - 90)) * delta_pitch
        delta_vz = math.cos(self.dtr(self.yaw_angle)) * delta_pitch + math.cos(self.dtr(self.yaw_angle - 90)) * delta_roll
        delta_vy = delta_hover

        self.velocity[0] += math.floor(delta_vx * 100) / 100
        self.velocity[1] += math.floor(delta_vz * 100) / 100
        self.velocity[2] += math.floor(delta_vy * 100) / 100

        # update position vector
        for i in range(len(self.velocity)): self.position[i] += self.velocity[i]

        # return ordi
        return self.ordi()

    def reset(self):
        self.position = np.random.randint(-self.bound, self.bound, [3])
        self.velocity = np.zeros([3])
        self.yaw_angle = 0
        return self.ordi()

    def sample_random_action(self):
        return int(np.random.randint(0, self.num_actions))

    def dtr(self, deg):
        return deg * (math.pi / 180)