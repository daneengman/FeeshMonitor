# These could also each be their own file

import random
import datetime

# for temperature sensor
import os
import glob
import time

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
        self.value = random.randint(0, 100)
        return self.get_value()

    def field_name(self):
        return f"Test value {self.name}"

class Time_sensor(Generic_sensor):
    def __init__(self, name=""):
        self.name = name
        self.update_value()

    def get_value(self) -> str:
        return self.value

    def update_value(self) -> str:
        self.value = datetime.datetime.now()
        return self.get_value()

    def field_name(self):
        return f"Time"

class Temperature_sensor:
    def __init__(self):
        """ Completes setup process for sensor """
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

        self.update_value()

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f

    def get_value(self):
        """ Returns last read value from sensor without reading it again """
        return self.value

    def update_value(self):
        """ Sets value to value read from sensor, and returns it """
        self.value = self.read_temp()[0]
        return self.get_value()

    def field_name(self) -> str:
        """ Returns the name of the field, such as temperature """
        return "Temperature"