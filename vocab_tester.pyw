# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:44:24 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Vocabulary testing application
Ver 0.1
"""

from modules.gui import *
from modules.api import *

root = Application(geometry = "453x236", title = "Vocabulary tester 0.1")

supposition = EntryField(root)
supposition.show(row = 0, column = 0, columnspan = 7, sticky = "W, E")

question_field = EntryField(root)
question_field.show(row = 0, column = 7, columnspan = 3, sticky = "W, E")

explanation = TextBox(root, width = 51, height = 12, wrap = "word")
explanation.show(row = 1, column = 2, rowspan = 7, columnspan = 8, sticky = "E")

status_bar = Inscription(root, text = "Ready to go!")
status_bar.show(row = 8, column = 0, columnspan = 10, sticky = "E, S")

actions = Handling(file_name = "lib/dict.csv", word_input = supposition, explanation = explanation, status_bar = status_bar, quiz = True, question = question_field)

button = Knob(root, text = "Reply", command = actions.implement_answer)
button.show(row = 1, column = 0, rowspan = 7, columnspan = 2, sticky = "N, S")

root.mainloop()
