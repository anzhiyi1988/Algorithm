import c45.c45 as c
import c45.data_set as data

import c45.treePlotter as tpo

lables_tmp = data.labels[:]

desicion_tree = c.create_tree(data.sample_set, lables_tmp)

print(desicion_tree)

tpo.createPlot(desicion_tree)

result = c.forecast_dd(data.test_set, desicion_tree, data.labels[:])

print(result)
