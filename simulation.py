from car import Car, IntelligentCar
from road import InfiniteRoad
from constants import CAR_SAFE_DIST

import random

class Simulation:

    def __init__(self):
        NUM_LANES = 5
        NUM_CARS = 20

        self.infinite_road = InfiniteRoad(NUM_LANES)

        for i in range(NUM_CARS):
            start_lane = random.choice(range(NUM_LANES))
            start_x = (i+1)*CAR_SAFE_DIST + 1
            c = Car()
            self.infinite_road.place_car(c, start_lane, start_x)

        c = IntelligentCar()
        self.infinite_road.place_car(c, int(NUM_LANES/2), 0)
        self.cam_x, self.cam_y = c.get_xy()
        self.infinite_road.set_camera_coords(self.cam_x, self.cam_y)

    def step(self):
        for lane in self.infinite_road.cars:
            for c in lane:
                c.step()
        self.infinite_road.update_state()
        return

    def reward(self):
        return 0

    def run(self):
        count = 1
        while True:
            self.step()
            count+=1

