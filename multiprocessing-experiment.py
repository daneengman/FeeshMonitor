from sensors import *
import datetime
from datalog import *

import numpy as np
import pandas as pd

import multiprocessing

from graphing import *

try:
    from camera import *
except:
    print("Probably not running on a Pi")

class Process_manager():
    def __init__(self, function, args):
        self.parent_pipe, self.child_pipe = multiprocessing.Pipe()
        self.process = multiprocessing.Process(target=function, args=(args, self.child_pipe,))
        self.process.start()

        # wait for initialization
        msg = self.parent_pipe.recv()
        print(msg)

    def send_msg(self, msg):
        self.parent_pipe.send(msg)

    def join(self):
        self.process.join()

def main():
    print("Starting up...")
    data_lock = multiprocessing.Lock()
    processes = {}
    processes["data_collection_manager"] = Process_manager(sensor_collection, data_lock)
    processes["graphing_manager"] = Process_manager(graphing, data_lock)
    processes["photographing_manager"] = Process_manager(photographing, data_lock)


    print("Running loop...")
    print("Press any key to end")

    msg = input()
    for process_manager in processes:
        processes[process_manager].send_msg(msg)
        processes[process_manager].join()
    
    print("test finished")
    

def sensor_collection(data_lock, child_pipe):
    data_lock.acquire()
    print("Initializing sensors....")
    test_sensors = [Time_sensor(), Test_sensor()]
    datalog = Datalog(test_sensors, True)
    data_lock.release()

    child_pipe.send("Sensor initialization finished")

    while True:
        datalog.update_values()
        datalog.append_values(data_lock)
        if child_pipe.poll(0.5):
            print("Ending data collection")
            break

    child_pipe.send("sensor_collection terminating")

def graphing(data_lock, child_pipe):
    graphing_o = Graphing()

    child_pipe.send("Graphing initialization finished")

    while True:
        graphing_o.make_graph(data_lock)
        if child_pipe.poll(5):
            print("Ending graph output")
            break

    child_pipe.send("graphing terminating")

def photographing(data_lock, child_pipe):
    camera_o = Camera()

    child_pipe.send("Camera initialization finished")

    while True:
        camera_o.take_picture()
        if child_pipe.poll(15):
            print("Ending photo capture")
            break

    child_pipe.send("Photographing terminating")

if __name__ == "__main__":
    main()