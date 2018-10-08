# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 14:26:34 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Auxiliary application that prints your current dictionary
Ver 3.0
"""

import csv

WORD = 0
EXPLANATION = 1

with open("lib/dict.csv") as f:
    csv_file = csv.reader(f)
    next(csv_file)
    dictionary = [(line[WORD], line[EXPLANATION]) for line in csv_file]
if dictionary:
    dictionary.sort()
    for line in dictionary:
        print(line[WORD], ":", line[EXPLANATION])
print("------------------\ntotal:", len(dictionary))
input()