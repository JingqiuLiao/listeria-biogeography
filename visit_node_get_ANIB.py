#!/usr/bin/env python
#Jingqiu Liao
#082019

# visit every node on the tree and get mean and standard deviation of ANI for each node 
# Prerequisite: pip install newick
# ANIB.xlsx is an excel file for ANI between each pair of isolates
# ANIb_dendrogram.newick is the tree file for ANI dendrogram of all isolates


import newick
import glob
import xlrd
import csv
import numpy as np
import xlwt 
from xlwt import Workbook
import statistics 

book = xlrd.open_workbook("ANIB.xlsx")
sheet = book.sheets()[0]

trees = newick.read("ANIb_dendrogram.newick")
print('finished reading newick')

counter = 0

class Visitor:
    '''
    Visit each node. Set its name then check for number of leaves.
    '''
    def __call__(self, node):
        global counter
        node.name = 'n_' + str(counter)
        print(node)
        counter += 1
        list_leaf = node.get_leaf_names()
        ani = []
        for i in range(sheet.nrows):
            if sheet.row_values(i)[0] in list_leaf and sheet.row_values(i)[1] in list_leaf:
                ani.append(sheet.row_values(i)[2])
        with open (node.name + '_ANIB.txt', 'a') as g:
            g.writelines('%s\n' % a for a in ani)
        with open(node.name + 'leaf.txt', 'a') as v:
            v.writelines('%s\n' % n for n in list_leaf)

class Predicate:
    '''
    Return True if node is not leaf and False otherwise.
    '''
    def __call__(self, node):
        return not node.is_leaf

# traverse starting from root
trees[0].visit(Visitor(), Predicate())

newick.write(trees, 'new_ANIb_dendrogram.newick')

# calculate mean and standard deviation of ANI for each node

for fname in sorted(glob.glob("*_ANIB.txt"), key=lambda fname: int(fname[2:-9])):
    list_ = []
    with open(fname, 'r') as f:
        lines = f.readlines()
        for x in lines:
            list_.append(float(x))
        mean = statistics.mean(list_)
        if len(list_) == 1:
            sd = 0
        else:
            sd = statistics.stdev(list_)
        with open('ANIB_node_mean_sd.txt', 'a') as v:
            v.write(fname[:-9] + "\t" + str(mean) + "\t" + str(sd) + "\n")