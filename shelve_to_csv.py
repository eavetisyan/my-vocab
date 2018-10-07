# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 18:03:08 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
From shelve to dictionary converter
Ver 1.2
"""
import shelve, csv

WORD = 0
EXPLANATION = 1

with shelve.open("lib/dict") as shelve_dictionary:
    try:
        csv_file = open("lib/dict.csv", "r")
        csv_file.close()
        input("The CSV-file is already exists")
    except IOError:
        with open("lib/dict.csv", "w") as csv_file:
            stats_header = [["Max guess", "Min guess", "Counter of maximals", "Counter of minimals"]]
            empty_row = [[]]
            dictionary_header = [["Word", "Explanation", "Guess"]]                                                                                                     # during the opening CSV-file
            header = stats_header + [[0, 0, len(shelve_dictionary), len(shelve_dictionary)]] + empty_row + dictionary_header
            csv_dictionary = csv.writer(csv_file, delimiter = ",", lineterminator = "\n")
            csv_dictionary.writerows(header)
            for line in shelve_dictionary.items():
                csv_dictionary.writerow([line[WORD], line[EXPLANATION], 0])
