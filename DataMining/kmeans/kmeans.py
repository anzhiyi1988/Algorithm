import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def init_random_center(k, row_max, n, data):
    """在元数据中随机获取k个点作为质心"""
    center = np.zeros([k, n])  # 建立一个空的k行n列的2维数组
    np.random.seed(5)
    for i in range(k):
        x = np.random.randint(row_max)
        center[i] = data.iloc[x]
    return center


def get_new_centers(data, k, col, dist_arr):
    """  从新计算质心，核心方法是numpy 的 mean """
    center_list = []
    axis_x, axis_y, axis_z = [], [], []
    col_min_index_arr = np.argmin(dist_arr, axis=0)  # 取每列的最小值索引，如果axis=1，则取每行的最小值索引
    for i in range(k):
        data_i = data.loc[col_min_index_arr == i]  # 拿到所有标记为true的是数据，整个数据的自己
        x, y, z = list(data_i.iloc[:, 1]), list(data_i.iloc[:, 2]), list(data_i.iloc[:, 3])
        axis_x.append(x)
        axis_y.append(y)
        axis_z.append(z)
        mean_center = np.mean(data_i, axis=0)  # 计算每列的平均值 ， 如果axis=1 则计算每行的平均值
        center_list.append(mean_center)
    center_arr = np.array(center_list).reshape(k, col)
    new_centers = np.nan_to_num(center_arr)
    return new_centers, axis_x, axis_y, axis_z


def get_distence(data, k, rows, center):
    """计算每个点距离每个k点的距离"""

    distence = []
    for i in range(k):
        for row in range(rows):
            x = np.array(data.iloc[row])
            a = x.T - center[i]  # 每个数字自动对应的相减
            dist = np.sqrt(np.sum(np.square(a)))  # 平方求和再开方
            distence.append(dist)

    dist_arr = np.array(distence).reshape(k, rows)  # 转换为k行rows列的数组
    return dist_arr


def kmeans_run(data, k, row, col, threshold):
    centers = init_random_center(k, row, col, data)
    new_centers = centers
    i = 0
    flag = True

    while flag:
        dist_arr = get_distence(data, k, row, new_centers)
        new_centers, axis_x, axis_y, axis_z = get_new_centers(data, k, col, dist_arr)
        print("centers:", centers)
        print("new centers:", new_centers)

        print("centers - new centers:", centers[-k:] - new_centers)
        _threshold = np.linalg.norm(centers[-k:] - new_centers)  # 求两个矩阵的范数

        i += 1

        draw2D(axis_x, axis_y, i, new_centers)
        # draw3D(axis_x, axis_y, axis_z, i, new_centers)

        if _threshold < threshold:
            flag = False
        else:
            centers = np.concatenate((centers, new_centers), axis=0)
    plt.show()


def draw2D(axis_x, axis_y, i, centers):
    plt.figure(1, [10, 10])  # 10*10英寸的画布
    p = plt.subplot(3, 3, i)
    p.set_title('Iteration' + str(i))
    p1 = p.scatter(axis_x[0], axis_y[0], c='r')
    p2 = p.scatter(axis_x[1], axis_y[1], c='g')
    p3 = p.scatter(axis_x[2], axis_y[2], c='b')
    p.scatter(centers[0, 1], centers[0, 2], c='r', s=550, marker='x')
    p.scatter(centers[1, 1], centers[1, 2], c='g', s=550, marker='x')
    p.scatter(centers[2, 1], centers[2, 2], c='b', s=550, marker='x')

    p.legend(handles=[p1, p2, p3], labels=['0', '1', '2'], loc='best')


def draw3D(axis_x, axis_y, axis_z, i, centers):
    plt.figure(2, [14, 10])
    p = plt.subplot(3, 3, i, projection='3d')
    p.set_title('3-D scatter' + str(i))

    p.scatter(axis_x[0], axis_y[0], axis_z[0], c='r', s=50)
    p.scatter(axis_x[1], axis_y[1], axis_z[1], c='g', s=50)
    p.scatter(axis_x[2], axis_y[2], axis_z[2], c='b', s=50)

    p.scatter(centers[0, 1], centers[0, 2], centers[0, 3], c='black', s=400, marker='x')
    p.scatter(centers[1, 1], centers[1, 2], centers[1, 3], c='purple', s=400, marker='x')
    p.scatter(centers[2, 1], centers[2, 2], centers[2, 3], c='yellow', s=400, marker='x')

    p.set_zlabel('Z')  # 坐标轴
    p.set_ylabel('Y')
    p.set_xlabel('X')
