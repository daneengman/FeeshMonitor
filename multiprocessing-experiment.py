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

def main():
    print("Starting up...")
    data_lock = multiprocessing.Lock()
    parent_pipe_data, child_pipe_data = multiprocessing.Pipe()
    data_collection_p = multiprocessing.Process(target=sensor_collection, args=(data_lock, child_pipe_data,))

    data_collection_p.start()

    # wait for sensors to initialize
    msg = parent_pipe_data.recv()
    print(msg)

    
    parent_pipe_graphing, child_pipe_graph = multiprocessing.Pipe()
    graphing_p = multiprocessing.Process(target=graphing, args=(data_lock, child_pipe_graph,))

    graphing_p.start()

    # wait for graphing to initialize
    msg = parent_pipe_graphing.recv()
    print(msg)


    print("Running loop...")
    print("Press any key to end")

    msg = input()
    parent_pipe_data.send(msg)
    parent_pipe_graphing.send(msg)

    data_collection_p.join()
    graphing_p.join()
    print("test finished")
    

def sensor_collection(data_lock, child_pipe_data):
    data_lock.acquire()
    print("Initializing sensors....")
    test_sensors = [Time_sensor(), Test_sensor()]
    datalog = Datalog(test_sensors, True)
    data_lock.release()

    child_pipe_data.send("Sensor initialization finished")

    while True:
        datalog.update_values()
        datalog.append_values(data_lock)
        if child_pipe_data.poll(0.5):
            print("Ending data collection")
            break

    child_pipe_data.send("sensor_collection terminating")

def graphing(data_lock, child_pipe_graph):
    graphing_o = Graphing()

    child_pipe_graph.send("Graphing initialization finished")

    while True:
        graphing_o.make_graph(data_lock)
        if child_pipe_graph.poll(5):
            print("Ending graph output")
            break

    child_pipe_graph.send("graphing terminating")

# def photographing(data_lock, child_pipe_photo):
#     camera_o = Camera()

#     child_pipe_photo.send("Camera initialization finished")

#     while True:
#         graphing_o.make_graph(data_lock)
#         if child_pipe_photo.poll(15):
#             print("Ending graph output")
#             break

#     child_pipe_photo.send("graphing terminating")

if __name__ == "__main__":
    main()