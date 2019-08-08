import pandas as pd
import numpy as np
import kmeans as km


# read file
data = pd.read_csv("../data/iris.csv")
data_arr = data.iloc[:, 1:5]  # get data 1 2 3 4 colums
row, col = np.shape(data_arr)  # get
k = 3
threshold = 0.1

new_centers, axis_x, axis_y, axis_z, centers = km.kmcluster(data_arr, k, row, col, threshold)
# # 2-Dplot
# plt.figure(2)
# plt.scatter(new_centers[0, 1], new_centers[0, 2], c='r', s=550, marker='x')
# plt.scatter(new_centers[1, 1], new_centers[1, 2], c='g', s=550, marker='x')
# plt.scatter(new_centers[2, 1], new_centers[2, 2], c='b', s=550, marker='x')
# p1, p2, p3 = plt.scatter(axis_x[0], axis_y[0], c='r'), plt.scatter(axis_x[1], axis_y[1], c='g'), plt.scatter(axis_x[2],
#                                                                                                              axis_y[2],
#                                                                                                              c='b')
# plt.legend(handles=[p1, p2, p3], labels=['0', '1', '2'], loc='best')
# plt.title('2-D scatter')
# plt.show()
