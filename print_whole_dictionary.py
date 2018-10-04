# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 14:26:34 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Auxiliary application that prints your current dictionary
Ver 2.0
"""

import csv
from itertools import islice

WORD = 0
EXPLANATION = 1

with open("lib/dict.csv") as f:
    csv_file = csv.reader(f)
    next(islice(csv_file, 3, None))
    dictionary = [[line[WORD], line[EXPLANATION]] for line in csv_file]
if dictionary:
    dictionary.sort()
    for line in dictionary:
        print(line[WORD], ":", line[EXPLANATION])
print("------------------\ntotal:", len(dictionary))
input()