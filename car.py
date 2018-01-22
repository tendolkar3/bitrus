import math
from constants import SIM_DT, ROAD_DRAG_COEFF, GAS_PEDAL_TO_ACC, BRAKE_PEDAL_TO_DEACC, CAR_SAFE_DIST, MAX_SAFE_VEL

class Car():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 0
        self.heading = 0
        self.start_time = 0
        self.road = None
        self.length = 4

    def get_xy(self):
        return self.x, self.y

    def set_xy(self, x, y):
        self.x = x
        self.y = y
        return x, y

    def set_heading(self, heading):
        self.heading = heading

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_road(self, road):
        self.road = road

    def __get_front_car_dy(self):
        lane = self.road.get_lane_from_y(self.y)
        cars = [c for c in self.road.cars[lane] if c != self]
        distances_from_front_cars = [(c.x - self.x) if c.x >= self.x else (self.road.max_length + c.x - self.x) for c in cars]
        return sorted(distances_from_front_cars)

    def __decide_control_inputs(self):
        steering_angle, gas, brake = 0, 0, 0
        distances = self.__get_front_car_dy()
        closest_car_distance = min(distances) if len(distances)>0 else CAR_SAFE_DIST+10
        if closest_car_distance < CAR_SAFE_DIST:
            brake = 3*(100*self.speed/(closest_car_distance+1))
            gas = 0
        else:
            if self.speed <= MAX_SAFE_VEL:
                gas = 3*(10*closest_car_distance/(self.speed+1))
                gas = gas if gas<5 and self.speed+gas*0.1<MAX_SAFE_VEL else 5
                brake = 0
            else:
                gas = 0
                brake = 3*(100*self.speed/(closest_car_distance+1))
        return steering_angle, gas, brake

    def __control_car(self, steering, gas, brake):
        front_wheel_x = self.x + self.length / 2 * math.cos(self.heading)
        front_wheel_y = self.y + self.length / 2 * math.sin(self.heading)
        back_wheel_x = self.x - self.length / 2 * math.cos(self.heading)
        back_wheel_y = self.y - self.length / 2 * math.sin(self.heading)

        self.speed += (
            gas * GAS_PEDAL_TO_ACC * SIM_DT - (
                brake * BRAKE_PEDAL_TO_DEACC * SIM_DT) - ROAD_DRAG_COEFF * self.speed * SIM_DT)
        self.speed = self.speed if self.speed > 0 else 0

        # update wheel positions
        front_wheel_x += self.speed * SIM_DT * math.cos(self.heading + steering)
        front_wheel_y += self.speed * SIM_DT * math.sin(self.heading + steering)
        back_wheel_x += self.speed * SIM_DT * math.cos(self.heading)
        back_wheel_y += self.speed * SIM_DT * math.sin(self.heading)

        # update car position and heading
        self.x = (front_wheel_x + back_wheel_x) / 2
        self.y = (front_wheel_y + back_wheel_y) / 2
        self.heading = math.atan2((front_wheel_y - back_wheel_y), (front_wheel_x - back_wheel_x))

        return

    def __clip_states(self):
        self.set_xy(self.x % self.road.max_length, self.y)

    def update_states(self):
        steering, gas, brake = self.__decide_control_inputs()
        self.__control_car(steering, gas, brake)
        self.__clip_states()
        return self.x, self.y, self.heading, self.speed

    def step(self):
        self.update_states()


class IntelligentCar(Car):
    def __init__(self):
        Car.__init__(self)

    def __decide_control_inputs(self):
        steering_angle, gas, brake = 0, 0, 0
        distances = self.__get_front_car_dy()
        closest_car_distance = min(distances)
        if closest_car_distance < CAR_SAFE_DIST:
            brake = 3 * (100 * self.speed / (closest_car_distance + 1))
            gas = 0
        else:
            if self.speed <= MAX_SAFE_VEL:
                gas = 3 * (10 * closest_car_distance / (self.speed + 1))
                gas = gas if gas < 5 and self.speed + gas * 0.1 < MAX_SAFE_VEL else 5
                brake = 0
            else:
                gas = 0
                brake = 3 * (100 * self.speed / (closest_car_distance + 1))
        return steering_angle, gas, brake