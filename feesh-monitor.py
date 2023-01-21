from sensors import *
import datetime
from datalog import *

import numpy as np
import pandas as pd

import multiprocessing



def main():
    print("Initializing...")
    test_sensors = [Time_sensor(), Temperature_sensor()]
    datalog = Datalog(test_sensors, True)

    print("Running loop...")
    print("Press any key to end")
    data_collection_p = multiprocessing.Process(target=data_collection, args = (datalog,))
    data_collection_p.start()


    print("test finished")
    datalog.make_graph()

def data_collection(datalog):
    while True:
        datalog.append_values()
        time.sleep(0.5)

if __name__ == "__main__":
    main()