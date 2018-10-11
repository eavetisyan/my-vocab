# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:44:24 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Vocabulary testing application
Ver 2.0
"""

from modules.gui import *
from modules.tester import *

root = Application(geometry = "412x262", title = "Vocabulary tester 2.0")

supposition = EntryField(root)
supposition.show(row = 0, column = 0, columnspan = 7, sticky = "W, E")

question_field = EntryField(root)
question_field.show(row = 0, column = 7, columnspan = 3, sticky = "W, E")

explanation = TextBox(root, width = 51, height = 12, wrap = "word")
explanation.show(row = 1, column = 0, rowspan = 7, columnspan = 10, sticky = "E")

status_bar = Inscription(root, text = "Enter your assumption of meaning of the right top word to the left top field")
status_bar.show(row = 9, column = 0, columnspan = 10, sticky = "E, S")

actions = Handling(file_name = "lib/dict.csv", supposition = supposition, explanation = explanation, status_bar = status_bar, question = question_field)

button = Knob(root, text = "Reply", command = actions.implement_an_answer)
button.show(row = 8, column = 0, columnspan = 10)

root.bind("<Return>", lambda _: actions.implement_an_answer())

root.mainloop()
