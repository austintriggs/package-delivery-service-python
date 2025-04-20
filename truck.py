import datetime


class Truck:
    def __init__(self, capacity=16, speed=18, packages=None, mileage=0, address="4001 South 700 East", depart_time=str(datetime.time(8, 0, 0))):
        if packages is None:
            packages = []
        self.capacity = capacity
        self.speed = speed
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time

    def __str__(self):
        return str(self.__dict__)