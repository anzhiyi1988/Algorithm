import pandas as pd
import numpy as np
from kmeans import *

# read file

if __name__ == "__main__":
    df_data = pd.read_csv("../data/iris.csv")
    df_data_new = df_data.iloc[:, 1:5]  # get data 1 2 3 4 colums
    row, col = np.shape(df_data_new)  # get
    k = 3
    threshold = 0.1
    kmeans.kmeans_run(df_data_new, k, row, col, threshold)
