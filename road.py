
class InfiniteRoad:
    def __init__(self, num_lanes):
        self.num_lanes = num_lanes
        self.lane_width = 4
        self.cars = [[] for _ in range(num_lanes)]
        self.max_length = 1000
        self.camera_coords = (0, 0)

    def place_car(self, car, start_lane=None, start_x=None):

        y = start_lane*self.lane_width + self.lane_width/2.0
        x = start_x % self.max_length

        car.set_xy(x, y)
        car.set_heading(0)
        car.set_road(self)

        self.__add_to_storage(car)

    def set_camera_coords(self, x, y):
        self.camera_coords = (x, y)

    def get_camera_coords(self):
        return self.camera_coords

    def __add_to_storage(self, car):
        x, y = car.get_xy()
        lane = self.get_lane_from_y(y)
        num_cars_in_lane = len(self.cars[lane])
        if num_cars_in_lane==0:
            self.cars[lane].append(car)
            return
        for i, existing_car in enumerate(self.cars[lane]):
            existing_car_x, existing_car_y = existing_car.get_xy()
            if x > existing_car_x:
                self.cars[lane].insert(i, car)
                return
        self.cars[lane].append(car)
        return

    def get_lane_from_y(self, y):
        return int(y // self.lane_width)

    def update_state(self):
        cars = [c for lane in self.cars for c in lane]
        self.cars = [[] for _ in range(self.num_lanes)]
        for c in cars:
            self.__add_to_storage(c)
