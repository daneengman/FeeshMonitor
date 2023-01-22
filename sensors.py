# These could also each be their own file

import random
import datetime

# for temperature sensor
import os
import glob
import time

from math import *

# # for camera
# from picamera import PiCamera
# import time

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
    def __init__(self, name="0", log=False):
        self.value = 100
        self.name = name
        self.log = log

    def get_value(self):
        return self.value

    def update_value(self):
        if not self.log:
            self.value = random.randint(0, 100)
        else:
            self.value = int(e**(random.random() * log(600, e)))
        return self.get_value()

    def field_name(self):
        return f"{self.name} (tst)"

class Time_sensor(Generic_sensor):
    def __init__(self, name=""):
        self.name = name
        self.update_value()

    def get_value(self) -> str:
        return str(self.value)

    def update_value(self) -> str:
        self.value = datetime.datetime.now()
        return self.get_value()

    def field_name(self):
        return f"Time"

class Temperature_sensor:
    def __init__(self):
        try:
            """ Completes setup process for sensor """
            os.system('modprobe w1-gpio')
            os.system('modprobe w1-therm')
            
            self.base_dir = '/sys/bus/w1/devices/'
            self.device_folder = glob.glob(self.base_dir + '28*')[0]
            self.device_file = self.device_folder + '/w1_slave'

            self.enabled = True
            self.update_value()
        except:
            print("Something is wrong with the temperature sensor.")
            self.enabled = False
            self.value = -1

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
        if self.enabled:
            try:
                self.value = self.read_temp()[1]
            except:
                print("Error with temperature sensor")
                self.value = -1
        
        return self.get_value()

    def field_name(self) -> str:
        """ Returns the name of the field, such as temperature """
        return "Temp"

class Arduino_sensor_heater:
    def __init__(self):
        try:
            """ Completes setup process for sensor """
            os.system('modprobe w1-gpio')
            os.system('modprobe w1-therm')
            
            self.base_dir = '/sys/bus/w1/devices/'
            self.device_folder = glob.glob(self.base_dir + '28*')[0]
            self.device_file = self.device_folder + '/w1_slave'

            self.enabled = True
            self.update_value()
        except:
            print("Something is wrong with the temperature sensor.")
            self.enabled = False
            self.value = -1

    def get_value(self):
        """ Returns last read value from sensor without reading it again """
        return self.value

    def update_value(self):
        """ Sets value to value read from sensor, and returns it """
        if self.enabled:
            try:
                self.value = -1
            except:
                print("Error with temperature sensor")
                self.value = -1
        
        return self.get_value()

    def field_name(self) -> str:
        """ Returns the name of the field, such as temperature """
        return "Heater"

    def turn_off(self):
        pass

    def turn_on(self):
        pass

class Arduino_sensor_co2:
    def __init__(self):
        self.enabled = True

    def get_value(self):
        """ Returns last read value from sensor without reading it again """
        return self.value

    def update_value(self):
        """ Sets value to value read from sensor, and returns it """
        if self.enabled:
            try:
                self.value = -1
            except:
                print("Error with co2 sensor")
                self.value = -1
        
        return self.get_value()

    def field_name(self) -> str:
        """ Returns the name of the field, such as temperature """
        return "CO2"