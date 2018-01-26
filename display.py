import pygame as pg
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, WHITE, PIXEL_PER_METER, CAR_LENGTH, CAR_SAFE_DIST
import math
from math import sqrt, atan2, cos, sin
from car import IntelligentCar
import sys


class Display:
    def __init__(self):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        pg.init()

        self.screen = pg.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32
        )
        # pg.display.set_caption("Bitrus")

        self.clock = pg.time.Clock()
        self.paused = False

        # self.sim = simulation

    def __draw_dashed_line(self, coords, wallcolor=(255, 255, 255)):
        length = sqrt((coords[1][1] - coords[0][1]) ** 2 + (coords[1][0] - coords[0][0]) ** 2)
        dash_length = 5.0
        slope = atan2((coords[1][1] - coords[0][1]), (coords[1][0] - coords[0][0]))
        for index in range(0, int(length / dash_length), 2):
            start = (coords[0][0] + (index * dash_length) * cos(slope), coords[0][1] +
                     (index * dash_length) * sin(slope))
            end = (coords[0][0] + ((index + 1) * dash_length) * cos(slope), coords[0][1] +
                   ((index + 1) * dash_length) * sin(slope))
            pg.draw.line(self.screen, wallcolor, start, end, 1)

    def draw_road(self, infinite_road):
        road_start = int(SCREEN_WIDTH/4)
        road_end = road_start + int(SCREEN_WIDTH/2)
        pg.draw.polygon(self.screen, BLACK, ((road_start, 0),(road_end, 0),(road_end, SCREEN_HEIGHT),(road_start, SCREEN_HEIGHT)))
        nl = infinite_road.num_lanes
        lane_width = SCREEN_WIDTH/(2*nl)
        for l in range(nl):
            if l==0:
                continue
            self.__draw_dashed_line(((l*lane_width+road_start,0), (l*lane_width+road_start,SCREEN_HEIGHT)))
        return

    def draw_car(self, infinite_road, car):
        road_start = int(SCREEN_WIDTH / 4)
        x,y = car.get_xy()
        y,x = (10*x), 10*y+road_start
        image = pg.transform.rotate(car.image, car.heading-90)
        rel_x,rel_y = infinite_road.get_camera_coords()
        # print(rel_y)
        x, y = x, y - rel_y + SCREEN_HEIGHT/2
        self.screen.blit(image, (x, y))
        return

    def draw(self, infinite_road, intelligent_car):
        self.screen.fill(WHITE)
        self.draw_road(infinite_road)
        cars = [c for lane in infinite_road.cars for c in lane]
        for car in cars:
            if isinstance(car, IntelligentCar):
                el_x, el_y = car.get_xy()
                infinite_road.set_camera_coords(el_y * 10, el_x * 10)
                break
        for car in cars:
            self.draw_car(infinite_road, car)

        # if lane==0:
        #     pass
        # # elif lane==infinite_road.num_lanes-1:
        #
        # else:
        rel_x, rel_y = intelligent_car.get_xy()
        lane = infinite_road.get_lane_from_y(rel_y)
        front_left = [(rel_x + 3*(CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+1)*infinite_road.lane_width),
                      (rel_x + 3 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+2) * infinite_road.lane_width),
                      (rel_x + 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+2) * infinite_road.lane_width),
                      (rel_x + 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+1) * infinite_road.lane_width)]
        lf = []
        for point in front_left:
            x,y = point
            y,x = 10*x, 10*y + int(SCREEN_WIDTH)/4
            x,y = x, y - rel_y + SCREEN_HEIGHT/2
            lf.append((x,y))

        front_right = [(rel_x + 3*(CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane)*infinite_road.lane_width),
                      (rel_x + 3 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane-1) * infinite_road.lane_width),
                      (rel_x + 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane-1) * infinite_road.lane_width),
                      (rel_x + 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane) * infinite_road.lane_width)]
        rf = []
        for point in front_right:
            x,y = point
            y,x = 10*x, 10*y + int(SCREEN_WIDTH)/4
            x,y = x, y - rel_y + SCREEN_HEIGHT/2
            rf.append((x,y))

        mid_right = [(rel_x - 1*(CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane)*infinite_road.lane_width),
                      (rel_x - 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane-1) * infinite_road.lane_width),
                      (rel_x + 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane-1) * infinite_road.lane_width),
                      (rel_x + 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane) * infinite_road.lane_width)]
        rm = []
        for point in mid_right:
            x,y = point
            y,x = 10*x, 10*y + int(SCREEN_WIDTH)/4
            x,y = x, y - rel_y + SCREEN_HEIGHT/2
            rm.append((x,y))
        mid_left = [(rel_x - 1*(CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+1)*infinite_road.lane_width),
                      (rel_x - 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+2) * infinite_road.lane_width),
                      (rel_x + 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+2) * infinite_road.lane_width),
                      (rel_x + 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+1) * infinite_road.lane_width)]
        lm = []
        for point in mid_left:
            x,y = point
            y,x = 10*x, 10*y + int(SCREEN_WIDTH)/4
            x,y = x, y - rel_y + SCREEN_HEIGHT/2
            lm.append((x,y))

        back_left = [(rel_x - 3*(CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+1)*infinite_road.lane_width),
                      (rel_x - 3 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+2) * infinite_road.lane_width),
                      (rel_x - 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+2) * infinite_road.lane_width),
                      (rel_x - 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane+1) * infinite_road.lane_width)]
        lb = []
        for point in back_left:
            x,y = point
            y,x = 10*x, 10*y + int(SCREEN_WIDTH)/4
            x,y = x, y - rel_y + SCREEN_HEIGHT/2
            lb.append((x,y))

        back_right = [(rel_x - 3*(CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane)*infinite_road.lane_width),
                      (rel_x - 3 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane-1) * infinite_road.lane_width),
                      (rel_x - 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane-1) * infinite_road.lane_width),
                      (rel_x - 1 * (CAR_LENGTH / 2 + CAR_SAFE_DIST), (lane) * infinite_road.lane_width)]
        rb = []
        for point in back_right:
            x, y = point
            y, x = 10*x, 10*y + int(SCREEN_WIDTH) / 4
            x, y = x, y - rel_y + SCREEN_HEIGHT / 2
            rb.append((x, y))

        print('drawing')
        pg.draw.polygon(self.screen, (0, 255, 0), lf, 3)
        pg.draw.polygon(self.screen, (0, 255, 0), rf, 3)
        pg.draw.polygon(self.screen, (0, 255, 0), rm, 3)
        pg.draw.polygon(self.screen, (0, 255, 0), lm, 3)
        pg.draw.polygon(self.screen, (0, 255, 0), rb, 3)
        pg.draw.polygon(self.screen, (0, 255, 0), lb, 3)

        pg.display.flip()

    # Todo: run method should not be on Display class
    def run(self, infinite_road):
        while True:
            # Limit frame speed to 30 FPS
            time_passed = self.clock.tick(30)
            if time_passed > 100:
                continue

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.paused = not self.paused

            if not self.paused:
                # self.sim.sim_step()
                self.draw(infinite_road)

            pg.display.flip()
        # return

    def quit(self):
        sys.exit()


# if __name__ == "__main__":
#     sim = Display()
    # cProfile.run('sim.run()')
    # sim.run()

# s = Simulation()
# with open("test.json", mode='w', encoding='utf-8') as feedsjson:
#
#     entry = {'name': args.name, 'url': args.url}
#     feeds.append(entry)
#     json.dump(feeds, feedsjson)
# s.run()

