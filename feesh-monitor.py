from sensors import *
import datetime
from datalog import *

import numpy as np
import pandas as pd

def main():
    print("Initializing...")
    test_sensors = [Time_sensor(), Temperature_sensor()]
    datalog = Datalog(test_sensors, True)

    print("Running loop...")
    for _ in range(10):
        datalog.append_values()
        time.sleep(0.5)
    print("test finished")
    datalog.make_graph()

if __name__ == "__main__":
    main()