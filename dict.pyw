# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 00:12:25 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Application that allows you to create and fill your own dictionary
Ver 2.2.1
"""

from modules.gui import *
from modules.api import *
    
root = Application(geometry = "449x145", title = "My own dictionary 2.2.1")
word_input = EntryField(root)
word_input.show(row = 0, column = 0)

explanation = TextBox(root, width = 40, height = 5, wrap = "word")
explanation.show(row = 0, column = 1, rowspan = 5)

status_bar = Inscription(root, text = "Ready to go!")
status_bar.show(row = 7, column = 1, columnspan = 6, sticky = "E, S")

operations = Handling(file_name = "lib/dict.csv", word_input = word_input, explanation = explanation, status_bar = status_bar)
    
buttons = {"Find word" : operations.find_word, "Add word" : operations.add_word, "Edit word" : operations.edit_word, "Delete word" : operations.delete_word}
root.create_stack_of_buttons(buttons, first_row = 1, column = 0)

root.mainloop()
