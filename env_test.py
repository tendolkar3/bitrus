from environment import Env
from car import IntelligentCar


env = Env()
env.render()
env._get_observation()
"""
for lane in env.simulation.infinite_road.cars:
    for car in lane:
        print(env.simulation.infinite_road.get_lane_from_y(car.y), car.get_xy(), isinstance(car, IntelligentCar))
"""

for i in range(100):
    action = ([-0.1],[1])
    inp = input()
    env.render()
    print(env.step(action))

