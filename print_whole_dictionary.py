# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 14:03:51 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Auxiliary application that prints your current dictionary
"""

import shelve
with shelve.open('lib/dict') as d:
    a = dict(sorted(d.items()))
    for s in a:
        print(s + ' : ' + a[s], end = '')
    print('--------------------\nTotal: ' + str(len(a)))
input()