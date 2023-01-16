from sensors import *
import datetime
from datalog import *

import numpy as np
import pandas as pd

def main():
    test_sensors = [Test_sensor(0), Test_sensor(1)]
    datalog = Datalog(test_sensors, True)

    print("Running loop...")
    for _ in range(10):
        continue
    print("test finished")

if __name__ == "__main__":
    main()