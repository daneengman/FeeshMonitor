from sensors import *
import datetime
from datalog import *

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import multiprocessing

from graphing import *

from camera import *
on_pi = is_enabled()

import pygame
import sys

"""
class Single_process():
    def __init__(self, function, args_list, pipes):
        self.parent_pipe, self.child_pipe = multiprocessing.Pipe()
        self.process = multiprocessing.Process(target=function, args=list(args_list))
        self.process.start()

        # wait for initialization
        msg = self.parent_pipe.recv()
        print(msg)

    def send_msg(self, msg):
        self.parent_pipe.send(msg)

    def join(self):
        self.process.join()

class Process_manager():
    def __init__(self):
        self.pipes = {}
        self.processes = {}

    def create_process(self, function, args_list, pipes):
        pipe_list = []
        for (pipe,pipe_side) in pipes:
            if pipe not in self.pipes:
                self.pipes[pipe] = multiprocessing.Pipe()
            pipe_list.append(self.pipes[pipe](pipe_side))
                
        self.processes[function.__name__] = Single_process(function, args_list, pipe_list)
    
    def message_all(self, msg):
        for process in self.processes:
            self.processes[process].send_msg(msg)
        
    def join_all(self):
        for process in self.processes:
            self.processes[process].join()

def main():
    print("Starting up...")
    data_lock = multiprocessing.Lock() # frankly this might not be necessary
    process_manager = Process_manager()
    process_manager.create_process(sensor_collection, [data_lock], [])
    process_manager.create_process(graphing, [data_lock], [(0,0)])
    process_manager.create_process(photographing, [data_lock], [(1,0)])
    process_manager.create_process(graphics, [data_lock], [(0,1),(1,1)])


    print("Running loop...")
    print("Press any key to end")

    msg = input()
    process_manager.message_all(msg)
    process_manager.join_all()
    
    print("test finished")
"""

dims = (width,height) = (800,480)

class Process_manager():
    def __init__(self, function, args):
        self.parent_pipe, self.child_pipe = multiprocessing.Pipe()
        args_f = tuple(args + [self.child_pipe])
        self.process = multiprocessing.Process(target=function, args=args_f)
        self.process.start()

        # wait for initialization
        msg = self.parent_pipe.recv()
        print(msg)

    def send_msg(self, msg):
        self.parent_pipe.send(msg)

    def join(self):
        self.process.join()

class Queue_message():
    def __init__(self, originator, destination, msg):
        self.originator = originator
        self.destination = destination
        self.msg = msg

def main():
    print("Starting up...")
    data_lock = multiprocessing.Lock()
    queue = multiprocessing.Queue()
    processes = {}
    functions = [sensor_collection, graphing, photographing, graphics]
    for function in functions:
        processes[function.__name__] = Process_manager(function, [data_lock, queue])


    print("Running loop...")
    print("Press any key to end")

    while True:
        msg = queue.get()
        if type(msg) == Queue_message:
            # print("successfully received message")
            processes[msg.destination.__name__].send_msg(msg.msg)

        if type(msg) == str:
            print(msg)
            if "end" in msg:
                break
    
    for process_manager in processes:
        processes[process_manager].send_msg(msg)
        processes[process_manager].join()
    
    print("test finished")
    

def sensor_collection(data_lock, queue, child_pipe):
    data_lock.acquire()
    print("Initializing sensors....")
    test_sensors = [Time_sensor(), Test_sensor(0), Test_sensor(1), Test_sensor(2)]
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

def graphing(data_lock, queue, child_pipe):
    graphing_o = Graphing()


    line_width = 4
    horizontal_ratio = 5/16
    vertical_ratio = 6/9.6
    plot_size = width*(1-horizontal_ratio)-line_width/2, height*vertical_ratio-line_width/2

    child_pipe.send("Graphing initialization finished")

    while True:
        graphing_o.make_graph(data_lock, plot_size)
        queue.put(Queue_message(graphing, graphics, "new graph"))
        if child_pipe.poll(5):
            print("Ending graph output")
            break

    child_pipe.send("graphing terminating")

def photographing(data_lock, queue, child_pipe):
    camera_o = Camera()

    child_pipe.send("Camera initialization finished")

    while True:
        camera_o.take_picture()
        if child_pipe.poll(15):
            print("Ending photo capture")
            break

    child_pipe.send("Photographing terminating")

def graphics(data_lock, queue, child_pipe):
    pygame.init()
    # screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    if on_pi:
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(dims)
    screen.fill((255,255,255))
    child_pipe.send("Graphics initialization finished")

    graph = [pygame.image.load(f"Graphs/{graph_path}") for graph_path in os.listdir("Graphs")][0]

    # screen
    line_width = 4
    horizontal_ratio = 5/16
    vertical_ratio = 6/9.6
    plot_size = width*(1-horizontal_ratio)-line_width/2, height*vertical_ratio-line_width/2
    pygame.draw.line(screen, (0,0,0), (width*horizontal_ratio,0), (width*horizontal_ratio,height), width=line_width)
    pygame.draw.line(screen, (0,0,0), (0,height*6/9.6), (width,height*6/9.6), width=line_width)
    pygame.draw.line(screen, (0,0,0), (0,height*2.4/9.6), (width*horizontal_ratio,height*2.4/9.6), width=line_width)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                queue.put("end from graphics")
                sys.exit()
        # screen.blit(graphs[0], (0, 0))
        if child_pipe.poll(0.1): # timing?  
            child_pipe.recv()
            # print([f"Graphs/{graph_path}" for graph_path in os.listdir("Graphs")]) debugging I guess
            graph = [pygame.image.load(f"Graphs/{graph_path}") for graph_path in os.listdir("Graphs")][0]
        screen.blit(graph, (width*horizontal_ratio + line_width/2,0))
        pygame.display.update()

if __name__ == "__main__":
    main()