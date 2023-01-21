import os
import datetime
import shutil

import pandas as pd
import matplotlib.pyplot as plt

class Graphing():
    def __init__(self):
        self.file_init()
    
    def file_init(self):
        if not os.path.exists("Graphs"):
            os.mkdir("Graphs")
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        if not os.path.exists("tmp/graphing"):
            os.mkdir("tmp/graphing")
        
    def make_graph(self, data_lock, dims):
        data_lock.acquire()
        path = self.copy_csv()
        data_lock.release()

        # probably need a graph file lock too eventually
        """ some sort of basic graph \\o.o/ """
        width,height = dims
        df = pd.read_csv(path, index_col = 0, parse_dates = True) # boy isn't this efficient
        # print(df)
        
        # px = 1/plt.rcParams['figure.dpi']  # pixel in inches
        # df.plot(
        #                 figsize = (dims[0]*px,dims[1]*px)) # adjust to whatever plot you want to see
        # plt.legend(['A', 'B', 'C'], loc='upper left')
        # # plt.show()
        # # plt.title("hello!")
        # plt.savefig(f'Graphs/Graph.PNG')
        # plt.close()

    def copy_csv(self):
        date = datetime.datetime.now().date() # issues with timezone?
        path_original = f"logs/{date}.csv"
        path_new = f"tmp/graphing/{date}.csv"
        shutil.copy(path_original, path_new)
        return path_new