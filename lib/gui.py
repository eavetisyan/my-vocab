# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 15:38:50 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Module for creating GUI application using Tkinter library
Ver 1.2
"""

from tkinter import Tk, Button, Entry, Text, Label

class Application(Tk):
    """Subclass of Tk that forms a window application"""
    def __init__(self, title, geometry, resizable = False):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(width = resizable, height = resizable)

    def create_stack_of_buttons(self, buttons, first_row, column, sticky = "W, E, N, S"):
        """Сreate buttons in a loop. The 'buttons' parameter is a dictionary
        whose keys are consists of buttons names,
        and values are names of a binded functions"""
        i = first_row
        for purpose in buttons:
            Knob(self, text = purpose, command = buttons[purpose]).show(row = i, column = column, sticky = sticky)
            i += 1

class Knob(Button):
    """Subclass of Button with simplified procedure of displaying"""
    def show(self, row, column, rowspan = 1, columnspan = 1, sticky = "W, E, N, S"):
        """Display an expanded button"""
        self.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan, sticky = sticky)

class EntryField(Entry):
    """Subclass of Entry with simplified procedures of displaying and text overwriting"""
    def show(self, row, column, columnspan = 1, sticky = "W, E, N, S"):
        """Display an expanded entry field"""
        self.grid(row = row, column = column, columnspan = columnspan, sticky = sticky)

    def overwrite(self, text):
        """Overwrite the content"""
        self.delete("0", "end")
        self.insert("0", text)

class Inscription(Label):
    """Subclass of Label with simplified procedures of displaying and text overwriting"""
    def show(self, row, column, columnspan = 1, sticky = "W, E, N, S"):
        """Display an expanded label"""
        self.grid(row = row, column = column, columnspan = columnspan, sticky = sticky)

    def overwrite(self, text):
        """Overwrite label's text"""
        self.config(text = text)

class TextBox(Text):
    """Subclass of Text with simplified procedures of displaying and text overwriting"""
    def show(self, row, column, rowspan = 1, columnspan = 1, sticky = "W, E, N, S"):
        """Display an expanded text box"""
        self.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan, sticky = sticky)

    def overwrite(self, text):
        """Overwrite the content"""
        self.delete("0.0", "end")
        self.insert("0.0", text)

if __name__ == "__main__":
    input("Please do not run this file. It's just a library")