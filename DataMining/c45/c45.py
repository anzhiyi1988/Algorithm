from math import log
import operator
import c45.treePlotter


def get_category(dd, i):
    """
    获取数据集的类别列

    :param dd: 数据集合，二维
    :param i: 目标类别所在列
    :return: 一维
    """
    return [c[i] for c in dd]


def get_attirbute(dd, i):
    """
    获取数据集的属性列

    :param dd:
    :param i:
    :return:
    """
    return [c[i] for c in dd]


def get_entropy(d):
    """
    计算给定数据集合的熵

    给定数据集的香农熵越大，数据集的混乱程度越大

    :param d: 数据集合，结构[x,y,x,....] ，集合内数据可重复
    :return:  数据集的熵
    """

    count = len(d)

    # key : 数据 ； value：数据在列表中出现的次数
    value_count_map = {}
    for value in d:

        if value not in value_count_map.keys():
            value_count_map[value] = 0
        value_count_map[value] += 1

    # 计算某类信息的信息熵
    entropy = 0.0
    for value in value_count_map:
        p = float(value_count_map[value]) / count  # 某个值的占比
        entropy -= p * log(p, 2)  # 所有值的信息量加在一起就是熵

    return entropy


def get_gain_ratio(dd, ai, ci):
    """
    获取某个属性的 信息增益比

    :param dd: 数据集
    :param ai: 属性列索引
    :param ci:  类别列索引
    :return:
    """

    category = get_category(dd, ci)
    attribute = get_attirbute(dd, ai)
    unique_attribute = set(attribute)

    category_emtropy = get_entropy(category)
    attribute_entropy = get_entropy(attribute)

    a_sum = 0.0
    for a in unique_attribute:
        sub_dd = split(dd, ai, a)
        sub_category = get_category(sub_dd, -1)
        sub_category_entropy = get_entropy(sub_category)
        a_sum += len(sub_dd) / float(len(dd)) * sub_category_entropy

    gain = category_emtropy - a_sum

    return gain / attribute_entropy


def majority_cnt(list):
    """
    暂时不描述

    :param list:
    :return:
    """

    pass


def split(data_set, i, feature):
    retDataSet = []
    for featVec in data_set:
        if featVec[i] == feature:
            reduceFeatVec = featVec[:i]
            reduceFeatVec.extend(featVec[i + 1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet


def get_best_feature(dd):
    """

    :param dd:
    :return:
    """

    attr_num = len(dd[0]) - 1


    best_gain_ratio = 0.0
    best_attr_idx = -1

    for i in range(attr_num):
        gain_ratin = get_gain_ratio(dd,i,-1)

        if(gain_ration)




def create_tree(sample_data, lables):
    """
    递归构建决策树

    :param sample_data: 样本数据
    :param lables: 样本数据标题
    :return:
    """

    last_col_list = [data[-1] for data in sample_data]

    # 如果特征都是一样的，没必要决策
    if last_col_list.count(last_col_list[0]) == len(last_col_list):
        return last_col_list
    if len(sample_data[0]) == 1:
        return majority_cnt(last_col_list)

    best_feat = get_best_feature(sample_data)
