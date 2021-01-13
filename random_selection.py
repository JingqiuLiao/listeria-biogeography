#!/usr/bin/env python
# 1/24/2019
# Jingqiu Liao
# Randomly select samples for each sampling grid
# Neg_samples.xlsx has a list of samples negative for Listeria and corresponding sampling grid

import xlrd
from random import choice

book = xlrd.open_workbook("Neg_samples.xlsx")
sheet = book.sheets()[0]
grid_dict = {}

for i in range(sheet.nrows):
    key = sheet.row_values(i)[1]
    value = sheet.row_values(i)[0]
    if key not in grid_dict:
        grid_dict[key] = []
    grid_dict[key].append(value)

sorted_keys = sorted(grid_dict)
sample = []

for x in range(0,19):
    if len(sample) < 312:
        for k in sorted_keys:
            if len(sample) < 312:
                try:
                    sample_k = choice(grid_dict[k])
                    with open ('neg_samples_selected.txt', 'a') as g:
                        g.write (sample_k + ' ' + str(int(k)) + '\n')
                    sample.append(sample_k)
                    grid_dict[k].remove(sample_k)
                except:
                    continue
