from car import Car, IntelligentCar
from road import InfiniteRoad
# from pedestrian import Pedestrian
# from traffic_signal import TrafficSignal

import random


class Simulation:

    def __init__(self):
        NUM_LANES = 5
        self.infinite_road = InfiniteRoad(NUM_LANES)
        NUM_CARS = 5
        for i in range(NUM_CARS):
            start_time = int(i)*100  # ms since simulation start
            start_lane = random.choice(range(NUM_LANES))
            start_x = int(i)*11
            c = Car()
            self.infinite_road.add(c, start_lane, start_x, start_time)

        c = IntelligentCar()
        self.infinite_road.add(c, int(NUM_LANES/2), 0, 0)
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
