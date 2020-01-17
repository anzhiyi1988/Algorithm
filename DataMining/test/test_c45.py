import c45.c45 as c
import c45.data_set as data

import c45.treePlotter as tpo

labels_tmp = data.labels[:]

decision_tree = c.create_tree(data.sample_set, labels_tmp)

print(decision_tree)

tpo.createPlot(decision_tree)

result = c.forecast_dd(data.test_set, decision_tree, data.labels[:])

print(result)
