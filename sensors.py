# These could also each be their own file

import random

class Generic_sensor:
    def __init__(self):
        """ Completes setup process for sensor """
        pass

    def get_value(self):
        """ Returns last read value from sensor without reading it again """
        pass

    def update_value(self):
        """ Sets value to value read from sensor, and returns it """
        pass

    def field_name(self) -> str:
        """ Returns the name of the field, such as temperature """
        pass


class Test_sensor(Generic_sensor):
    def __init__(self, name=0):
        self.value = 100
        self.name = name

    def get_value(self) -> int:
        return self.value

    def update_value(self) -> int:
        return random.randint(0, 100)

    def field_name(self):
        return f"Test value {self.name}"