# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 18:03:08 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
From shelve to CSV dictionary converter
Ver 2.0
"""

import shelve, csv

WORD = 0
EXPLANATION = 1

try:
    csv_file = open("lib/dict.csv", "r")
    csv_file.close()
    input("The CSV-file is already exists")
except IOError:
    header = ["Word", "Explanation", "Guess"]
    with shelve.open("lib/dict") as shelve_dictionary:
        with open("lib/dict.csv", "w") as csv_file:
            csv_dictionary = csv.writer(csv_file, delimiter = ",", lineterminator = "\n")
            csv_dictionary.writerow(header)
            for line in shelve_dictionary.items():
                csv_dictionary.writerow([line[WORD], line[EXPLANATION], 0])
