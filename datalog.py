from sensors import * # maybe idk
import csv
import datetime
import os

# The plan: create a csv file for every day, and log all that data into the 
# csv file

class Datalog:
    def __init__(self, sensors, reset = False):
        self.sensors = sensors # lol is there a better way to do this
        self.open_file(reset)

    def open_file(self, reset):
        date = datetime.date.isoformat(datetime.datetime.now()) # issues with timezone?
        if not os.path.exists("logs"):
            os.mkdir("logs")
        filename = f"logs/{date}.csv"
        if not reset and os.path.exists(filename):
            self.file = open(filename, "a")
        else:
            self.file = open(filename, "w")
            self.write_headers()

    def write_headers(self):
        fields = [sensor.field_name() for sensor in self.sensors]
        csvwriter = csv.writer(self.file)
        csvwriter.writerow(fields)