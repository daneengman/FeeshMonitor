from sensors import * # maybe idk
import csv
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

# try:
#     from camera import *
# except:
#     print("Probably not running on a Pi")

# The plan: create a csv file for every day, and log all that data into the 
# csv file

class frame:
    pass


class Datalog:
    def __init__(self, sensors, reset = False):
        self.sensors = sensors # lol is there a better way to do this
        if not os.path.exists("logs"):
            os.mkdir("logs")
        self.get_filepath(reset)

    def get_filepath(self, reset = False):
        date = datetime.datetime.now().date() # issues with timezone?
        self.filepath = f"logs/{date}.csv"
        if reset or not os.path.exists(self.filepath):
            with open(self.filepath, "w") as file:
                self.write_headers(file)

    def write_headers(self, file):
        fields = [sensor.field_name() for sensor in self.sensors]
        csvwriter = csv.writer(file)
        csvwriter.writerow(fields)

    def update_values(self):
        self.values = [sensor.update_value() for sensor in self.sensors]
        
    def get_values(self):
        return dict([(sensor.field_name(), sensor.get_value()) for sensor in self.sensors])

    def append_values(self, file_lock):
        file_lock.acquire()
        self.get_filepath()
        with open(self.filepath, "a") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(self.values)
            # add it to some other data structure?
        file_lock.release()

    # this could be improved
    # deprecated
    # def make_graph(self):
    #     """ some sort of basic graph \\o.o/ """
    #     df = pd.read_csv(self.filename, index_col = 0, parse_dates = True) # boy isn't this efficient
    #     print(df)

    #     df["Test value 0"].plot() # adjust to whatever plot you want to see
    #     # plt.show()
    #     plt.savefig('COOL_GRAPH.PNG')



    # this could be realistically moved to camera
    # deprecated
    # def take_photo(self):
    #     date = datetime.datetime.now().date() # issues with timezone?
    #     if not os.path.exists("photos"):
    #         os.mkdir("photos")
    #     photo_filepath = f"photos/{date}.png"
    #     self.camera.take_picture(photo_filepath)