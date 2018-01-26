from car import Car, IntelligentCar
from road import InfiniteRoad
from constants import CAR_SAFE_DIST, MAX_SAFE_VEL
import numpy as np
import random


class Simulation:

    def __init__(self):
        self.NUM_LANES = 5
        self.NUM_CARS = 20
        self.cam_x = None
        self.cam_y = None
        self.infinite_road = InfiniteRoad(self.NUM_LANES)

        for i in range(self.NUM_CARS):
            start_lane = random.choice(range(self.NUM_LANES))
            #Todo: randomize this
            start_x = (i+1)*CAR_SAFE_DIST + 1
            c = Car()
            self.infinite_road.place_car(c, start_lane, start_x)

        c = IntelligentCar()
        self.intelligent_car = c
        self.infinite_road.place_car(c, int(self.NUM_LANES/2), 0)
        self.cam_x, self.cam_y = c.get_xy()
        self.infinite_road.set_camera_coords(self.cam_x, self.cam_y)

    def sim_step(self, action):
        for lane in self.infinite_road.cars:
            for c in lane:
                if not isinstance(c, IntelligentCar):
                    c.step()
                else:
                    c.step(action)

        try:
            self.infinite_road.update_state()
        except IndexError:
            return False

        return self.get_status(self.intelligent_car)

    def get_status(self, car):
        """
        determines if the car is still in the game or violated any rules
        :param car:
        :return:
        """
        status = True
        x, y = car.get_xy()
        lane = self.infinite_road.get_lane_from_y(y)
        if car.speed > MAX_SAFE_VEL:
            print('vel')
            status = False
        elif (lane < 0) or (lane >= self.NUM_LANES):
            print('lane')
            status = False
        else:
            ind = self.infinite_road.cars[lane].index(car)

            if ind == len(self.infinite_road.cars[lane]) - 1 and ind == 0:
                status = True

            elif ind == len(self.infinite_road.cars[lane])-1:
                front_car = self.infinite_road.cars[lane][ind-1]
                if abs(car.x - front_car.x) <= car.length + CAR_SAFE_DIST/2:
                    print('front')
                    status = False

            elif ind == 0:
                back_car = self.infinite_road.cars[lane][ind+1]
                if abs(car.x - back_car.x) <= car.length + CAR_SAFE_DIST/2:
                    print('back')
                    status = False

            else:
                front_car = self.infinite_road.cars[lane][ind-1]
                back_car = self.infinite_road.cars[lane][ind+1]
                if abs(car.x - back_car.x) <= car.length + CAR_SAFE_DIST / 2:
                    print('back')
                    status = False
                if abs(car.x - front_car.x) <= car.length + CAR_SAFE_DIST/2:
                    print('front')
                    status = False

        return status

    def get_reward(self):

        reward = 0
        base_x, base_y = self.intelligent_car.get_xy()
        # base_lane = self.infinite_road.get_lane_from_y(base_y)

        for lane in self.infinite_road.cars:
            for c in lane:
                if not isinstance(c, IntelligentCar):
                    check_x, check_y = c.get_xy()
                    if check_x < base_x:
                        reward += 1

        return reward

    def get_observation(self):
        car = self.intelligent_car
        x, y = car.get_xy()
        lane = self.infinite_road.get_lane_from_y(y)
        if lane < 0 or lane >= self.infinite_road.num_lanes:

            raise IndexError

        ind = self.infinite_road.cars[lane].index(car)

        if ind == len(self.infinite_road.cars[lane]) - 1 and ind == 0:
            print("case 1")
            front_car = None
            front_front_car = None

        elif ind == len(self.infinite_road.cars[lane]) - 1:
            print("case 2")
            front_car = self.infinite_road.cars[lane][ind - 1]
            if ind - 2 > 0:
                front_front_car = self.infinite_road.cars[lane][ind-2]
            else:
                front_front_car = None

        elif ind == 0:
            print("case 3")
            front_car = None
            front_front_car = None

        else:
            print("case 4")
            front_car = self.infinite_road.cars[lane][ind - 1]
            if ind-2 > 0:
                front_front_car = self.infinite_road.cars[lane][ind-2]
            else:
                front_front_car = None

        if front_car is not None:
            front = np.array([front_car.x])
        else:
            front = np.array([CAR_SAFE_DIST*10])
        if front_front_car is not None:
            front_front = np.array([front_front_car.x])
        else:
            front_front = np.array([CAR_SAFE_DIST*10])

        right_0 = np.array([0])
        right_1 = np.array([0])
        right_2 = np.array([0])
        left_0 = np.array([0])
        left_1 = np.array([0])
        left_2 = np.array([0])
        left_lane = None
        right_lane = None

        if lane == 0:
            right_lane = self.infinite_road.cars[lane+1]
        elif lane == self.infinite_road.num_lanes-1:
            left_lane = self.infinite_road.cars[lane - 1]
        elif 0 < lane < self.infinite_road.num_lanes:
            right_lane = self.infinite_road.cars[lane+1]
            left_lane = self.infinite_road.cars[lane-1]
        else:
            right_0 = np.array([1])
            right_1 = np.array([1])
            right_2 = np.array([1])
            left_0 = np.array([1])
            left_1 = np.array([1])
            left_2 = np.array([1])

        if right_lane is not None:
            for r_car in right_lane:
                if (r_car.x < x - 1*(car.length / 2 + CAR_SAFE_DIST)) and (r_car.x > x - 3*(car.length / 2 + CAR_SAFE_DIST)):
                    right_0 = np.array([1])
                if (r_car.x < x + 1*(car.length / 2 + CAR_SAFE_DIST)) and (r_car.x > x - 1*(car.length / 2 + CAR_SAFE_DIST)):
                    right_1 = np.array([1])
                if (r_car.x < x + 3*(car.length / 2 + CAR_SAFE_DIST)) and (r_car.x > x + 1*(car.length / 2 + CAR_SAFE_DIST)):
                    right_2 = np.array([1])

        if left_lane is not None:
            for l_car in left_lane:
                if (l_car.x < x - 1 * (car.length / 2 + CAR_SAFE_DIST)) and (l_car.x > x - 3 * (car.length / 2 + CAR_SAFE_DIST)):
                    left_0 = np.array([1])
                if (l_car.x < x + 1 * (car.length / 2 + CAR_SAFE_DIST)) and (l_car.x > x - 1 * (car.length / 2 + CAR_SAFE_DIST)):
                    left_1 = np.array([1])
                if (l_car.x < x + 3 * (car.length / 2 + CAR_SAFE_DIST)) and (l_car.x > x + 1 * (car.length / 2 + CAR_SAFE_DIST)):
                    left_2 = np.array([1])

        observation = tuple((front, front_front, right_0, right_1, right_2, left_0, left_1, left_2))

        return observation

    # def run(self):
    #     count = 1
    #     while True:
    #         self.sim_step()
    #         count+=1
    #
