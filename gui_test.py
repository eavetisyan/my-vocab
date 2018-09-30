# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 21:20:29 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Testing of refactored GUI-code
"""

import modules.gui

def boo():
    print("boo!")

root = Application(geometry = "449x120", title = "My own dictionary")

word_input = EntryField(root)
word_input.show(row = 0, column = 0, sticky = "W, E, N, S")

buttons = {"Find word" : boo, "Add word" : boo, "Delete word" : boo}
root.create_stack_of_buttons(buttons, first_row = 1, column = 0)

explanation = TextBox(root, width = 40, height = 5, wrap = "word")
explanation.show(row = 0, column = 1, rowspan = len(buttons) + 2, sticky = "W, E, N, S")

status_bar = Inscription(root, text = "Ready to go!")
status_bar.show(row = 6, column = 1, columnspan = 6, sticky = "E, S")

root.mainloop()