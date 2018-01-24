from car import Car


class DoublyLinked(object):

    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
        self.length = 0

    def insert(self, car):

        if self.head is None:
            self.head = car
            car.prev = None
            self.tail = car
            car.next = None
            self.length += 1
            return
        else:
            temp_car = self.head

            # Todo: to optimize
            # if car.x <
            #
            # while temp_car.next is not None:
            #     if car.x > temp_car.x:
            #         break
            #     else:
            #         temp_car = temp_car.next


