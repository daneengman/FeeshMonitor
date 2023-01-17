from sensors import * # maybe idk
import csv
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

# The plan: create a csv file for every day, and log all that data into the 
# csv file

class Datalog:
    def __init__(self, sensors, reset = False):
        self.sensors = sensors # lol is there a better way to do this
        self.file_init(reset)

    def file_init(self, reset):
        date = datetime.datetime.now().date() # issues with timezone?
        if not os.path.exists("logs"):
            os.mkdir("logs")
        self.filename = f"logs/{date}.csv"
        if reset or not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                self.write_headers(file)

    def write_headers(self, file):
        fields = [sensor.field_name() for sensor in self.sensors]
        csvwriter = csv.writer(file)
        csvwriter.writerow(fields)

    def append_values(self):
        with open(self.filename, "a") as file:
            csvwriter = csv.writer(file)
            values = [sensor.update_value() for sensor in self.sensors]
            csvwriter.writerow(values)
            # add it to some other data structure?

    def make_graph(self):
        """ some sort of basic graph \o.o/ """
        df = pd.read_csv(self.filename, index_col = 0, parse_dates = True) # boy isn't this efficient
        print(df)

        df["Test value 0"].plot() # adjust to whatever plot you want to see
        plt.show()