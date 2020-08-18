import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        ext = os.path.splitext(self.photo_file_name)[1]
        if ext in (".jpg", ".jpeg", ".png", ".gif"):
            return ext


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'car'
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        self.body_length = float(0)
        self.body_width = float(0)
        self.body_height = float(0)

        try:
            body_list = body_whl.split("x")
            self.body_length, self.body_width, self.body_height = [float(body) for body in body_list]
        except ValueError:
            pass

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        read_list = list([row for row in reader])
    title, body = read_list[0], read_list[1:]
    new_list = list([dict(zip(title, car)) for car in body])
    for car in new_list:
        car = dict((key, value) for key, value in car.items() if value or key == "body_whl")
        try:
            c_type = car["car_type"]
            if c_type == 'car':
                car_obj = Car(car["brand"], car["photo_file_name"], float(car["carrying"]), int(car["passenger_seats_count"]))
            elif c_type == 'truck':
                car_obj = Truck(car["brand"], car["photo_file_name"], float(car["carrying"]), car["body_whl"])
            elif c_type == 'spec_machine':
                car_obj = SpecMachine(car["brand"], car["photo_file_name"], float(car["carrying"]), car["extra"])
            else:
                continue
            if not car_obj.get_photo_file_ext():
                continue
            car_list.append(car_obj)
        except Exception:
            pass
    return car_list
