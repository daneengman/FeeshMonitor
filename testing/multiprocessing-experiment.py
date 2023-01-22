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
            processes[msg.destination.__name__].send_msg(msg)

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
    test_sensors = [Time_sensor(), Test_sensor("Temp"), Test_sensor("CO2", log = True)]
    datalog = Datalog(test_sensors, True)
    datalog.update_values()
    data_lock.release()
    while True:
        continue

    child_pipe.send("Sensor initialization finished")

    while True:
        datalog.update_values()
        queue.put(Queue_message(sensor_collection, graphics, datalog.get_values()))
        # queue.put(Queue_message(sensor_collection, graphics, values)) # TODO
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
    disabled = False
    try:
        camera_o = Camera()
    except:
        print("Camera did not work")
        disabled = True

    child_pipe.send("Camera initialization finished")

    while True:
        if disabled:
            continue
        camera_o.take_picture()
        if child_pipe.poll(15):
            print("Ending photo capture")
            break

    child_pipe.send("Photographing terminating")

def graphics(data_lock, queue, child_pipe):
    pygame.init()
    # screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    if on_pi:
        try:
            os.environ["DISPLAY"] = ":0"
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        except:
            screen = pygame.display.set_mode(dims)
    else:
        screen = pygame.display.set_mode(dims)
    screen.fill((255,255,255))
    child_pipe.send("Graphics initialization finished")

    graph = [pygame.image.load(f"Graphs/{graph_path}") for graph_path in os.listdir("Graphs")][0]
    values = {}
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 40)
    # screen
    line_width = 4
    horizontal_ratio = 5/16
    vertical_ratio = 6/9.6
    plot_size = width*(1-horizontal_ratio)-line_width/2, height*vertical_ratio-line_width/2
    # should this be in some redraw all function

    
    


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                queue.put("end from graphics")
                sys.exit()
        # screen.blit(graphs[0], (0, 0))
        if child_pipe.poll(0.1): # timing?  
            msg = child_pipe.recv()
            if msg.originator == graphing:
                # print([f"Graphs/{graph_path}" for graph_path in os.listdir("Graphs")]) debugging I guess
                data_lock.acquire()
                graph = [pygame.image.load(f"Graphs/{graph_path}") for graph_path in os.listdir("Graphs")][0]
                data_lock.release()
            if msg.originator == sensor_collection:
                values = msg.msg
                # num_items = len(values)
                # for key in values:
                #     print(key, values[key])
        screen.fill((255,255,255))
        pygame.draw.line(screen, (0,0,0), (width*horizontal_ratio,0), (width*horizontal_ratio,height), line_width)
        pygame.draw.line(screen, (0,0,0), (0,height*6/9.6), (width,height*6/9.6), line_width)
        pygame.draw.line(screen, (0,0,0), (0,height*2.4/9.6), (width*horizontal_ratio,height*2.4/9.6), line_width)

        origin = (horizontal_ratio * width + line_width/2, vertical_ratio * height + line_width/2)
        draw_values(origin, width-origin[0], height-origin[1], values, screen, my_font)

        screen.blit(graph, (width*horizontal_ratio + line_width/2,0))


        pygame.display.update()

def draw_values(origin, width, height, values, screen, my_font):
    num_items = len(values)
    for key in values:
        if key == 'Time':
            # value = datetime.datetime.strptime(values[key], "%Y-%m-%d %H:%M:%S.%f").time().isoformat(timespec='seconds')
            value = datetime.datetime.now().time().isoformat(timespec='seconds')
        else:
            value = values[key]
        text_surface = my_font.render(f'{key}', False, (0, 0, 0))
        this_origin = (origin[0] + (width/num_items)/10, origin[1] + height/10)
        screen.blit(text_surface, this_origin)

        text_surface = my_font.render(f'{value}', False, (0, 0, 0))
        this_origin = (origin[0] + (width/num_items)/10, origin[1] + height/2)
        screen.blit(text_surface, this_origin)
        origin = (origin[0] + width/num_items, origin[1])
        # print(origin)

import serial
import time
import os
import glob

def outputs(data_lock, queue, child_pipe):
    print("Initializing the death box...")
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    child_pipe.send("Graphics initialization finished")
   
    msg = child_pipe.recv()
    if msg.originator == graphing:
        # print([f"Graphs/{graph_path}" for graph_path in os.listdir("Graphs")]) debugging I guess
        data_lock.acquire()
        graph = [pygame.image.load(f"Graphs/{graph_path}") for graph_path in os.listdir("Graphs")][0]
        data_lock.release()
    if msg.originator == sensor_collection:
        values = msg.msg

    while True:
        target = 72
        
        if current < target - 1:
            print("turning on heater")
            ser.write(b"high\n")
        elif current > target + 1:
            print("turning off heater")
            ser.write(b"low\n")
        line = ser.readline().decode('utf-8')
        print(line)
        time.sleep(1)

if __name__ == "__main__":
    main()