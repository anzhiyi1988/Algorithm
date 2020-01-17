from math import log
import operator


def get_category(dd, i):
    """
    获取数据集的类别列

    :param dd: 数据集合，二维
    :param i: 目标类别所在列
    :return: 一维
    """
    return [c[i] for c in dd]


def get_column_values(dd, idx):
    """
    获取一个数据集指定列的所有值

    :param dd:  一个二维数组
    :param idx:  获取第idx列值
    :return:  返回一个一维list
    """
    return [c[idx] for c in dd]


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
    attribute = get_column_values(dd, ai)
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


def majority_cnt(class_list):
    """
    输入：分类类别列表
    输出：子节点的分类
    描述：数据集已经处理了所有属性，但是类标签依然不是唯一的，
          采用多数判决的方法决定该子节点的分类
    """
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reversed=True)
    return sorted_class_count[0][0]


def split(data_set, i, feature):
    ret_data_set = []
    for featVec in data_set:
        if featVec[i] == feature:
            reduce_feat_vec = featVec[:i]
            reduce_feat_vec.extend(featVec[i + 1:])
            ret_data_set.append(reduce_feat_vec)
    return ret_data_set


def get_best_attr_idx(dd):
    """

    :param dd:
    :return:
    """

    attr_num = len(dd[0]) - 1

    best_gain_ratio = 0.0
    best_attr_idx = -1

    print("计算信息增益比数据：", dd)
    for i in range(attr_num):
        gain_ratio = get_gain_ratio(dd, i, -1)

        print("信息第", i, "列增益比:", gain_ratio)

        if gain_ratio > best_gain_ratio:
            best_gain_ratio = gain_ratio
            best_attr_idx = i
    return best_attr_idx


def create_tree(sample_data, labels):
    """
    递归构建决策树

    :param sample_data: 样本数据
    :param labels: 样本数据标题
    :return:
    """

    last_col_list = [data[-1] for data in sample_data]

    # 如果特征都是一样的，没必要决策
    if last_col_list.count(last_col_list[0]) == len(last_col_list):
        return last_col_list[0]
    if len(sample_data[0]) == 1:
        return majority_cnt(last_col_list)

    best_attr_idx = get_best_attr_idx(sample_data)

    best_attr_label = labels[best_attr_idx]

    my_tree = {best_attr_label: {}}

    del (labels[best_attr_idx])

    best_attr_values = [data[best_attr_idx] for data in sample_data]

    unique_values = set(best_attr_values)

    for value in unique_values:
        sub_labels = labels[:]
        sub_dd = split(sample_data, best_attr_idx, value)
        sub_tree = create_tree(sub_dd, sub_labels)
        print(sub_tree)
        my_tree[best_attr_label][value] = sub_tree
        print(my_tree)
    return my_tree


def forecast(row, decision_tree, labels):
    """
    把每一行代入树中

    :param row:
    :param decision_tree:
    :param labels:
    :return:
    """

    first_label = list(decision_tree.keys())[0]
    sub_tree = decision_tree[first_label]
    col_idx = labels.index(first_label)

    r = ""

    for key in sub_tree.keys():
        if row[col_idx] == key:
            if type(sub_tree[key]).__name__ == "dict":
                r = forecast(row, sub_tree[key], labels)
            else:
                r = sub_tree[key]
    return r


def forecast_dd(dd, decision_tree, lables):
    result = []
    for row in dd:
        result.append(forecast(row, decision_tree, lables))
    return result
