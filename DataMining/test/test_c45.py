import c45.c45 as c
import c45.data_set as data

lables_tmp = data.labels[:]

desicion_tree = c.create_tree(data.sample_set, lables_tmp)
