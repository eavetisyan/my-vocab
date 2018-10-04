# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 20:42:21 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Application that allows you to create and fill your own dictionary
Ver 2.0
"""

from modules.gui import *
from itertools import islice
import csv

STATUS_LINE = 1

WORD = 0
VALUE = 1
EXPLANATION = 0
GUESS = 1

DESCRIPTION = 1
COUNTER = 2

class Handling():
    """Dictionary management procedures"""
    def __init__(self, file_name, word_input, explanation, status_bar):
        """Get dictionary from CSV-file"""
        self.__file_name = file_name
        self.__word_input = word_input
        self.__explanation = explanation
        self.__status_bar = status_bar
        with open(file_name, "r") as file:                                                                                      # Open file for reading just for copying stats and dictionary to RAM
            readed_csv = csv.reader(file)
            self.__max_guess, self.__min_guess, self.__quant_max, self.__quant_min = self.__read_thru_n_strings(readed_csv)     # Jump to the stats string 
            self.__read_thru_n_strings(readed_csv)                                                                              # Cut off headers and stats
            self.__dictionary = {line[WORD] : [line[DESCRIPTION], int(line[COUNTER])] for line in readed_csv}                   # Constructing dictionary as "word : [explanation, guess]" structure
    
    def __read_thru_n_strings(self, iterable_object, n = 1):
        """Jump from current line to n-distance"""
        return next(islice(iterable_object, n, None))
    
    def __ovewrite_dictionary(self):
        """Overwriting an existing dictionary"""
        stats_header = [["Max guesses", "Min guesses", "Quantity of maximals", "Quantity of minimals"]]                         # Headers and stats
        dictionary_header = [["Word", "Explanation", "Guess"]]                                                                  # which were cutted off
        empty_row = [[]]                                                                                                        # during the opening CSV-file
        header = stats_header + [[self.__max_guess, self.__min_guess, self.__quant_max, self.__quant_min]] + empty_row + dictionary_header
        with open(self.__file_name, "w") as file:
            csv_file = csv.writer(file, delimiter = ",", lineterminator = "\n")
            csv_file.writerows(header)                                                                                          # Write headers and stats to CSV
            for row in self.__dictionary_lines(self.__dictionary):
                csv_file.writerow(row)                                                                                          # Write dictionary to CSV
    
    def __dictionary_lines(self, dictionary):
        """Get next dictionary line as list"""
        for line in dictionary.items():
            dictionary_string = [line[WORD], line[VALUE][EXPLANATION], line[VALUE][GUESS]]
            yield dictionary_string
    
    def __get_word(self):
        """Pop the word from text entry and set the first letter to upper case"""
        word = self.__word_input.get()
        if word:
            word = word[0].upper() + word[1:]                                                                                   # This is because the text entry may contains more than one word
        return word
    
    def find_word(self):
        """Finding word function"""
        word = self.__get_word()
        if word:
            try:
                self.__explanation.overwrite(self.__dictionary[word][EXPLANATION])
                self.__status_bar.overwrite(word + " - found!")
            except KeyError:
                self.__status_bar.overwrite("There is no '" + word + "' in the dictionary")
        else:
            self.__status_bar.overwrite("Please enter the word")

    def add_word(self):
        """Add word to dictionary"""
        word = self.__get_word()
        if word:
            self.__dictionary[word] = [self.__explanation.get('0.0', 'end - 1c'), 0]
            self.__ovewrite_dictionary()
            self.__status_bar.overwrite(word + " - added to dictionary")
        else:
            self.__status_bar.overwrite("Please enter the word")

    def delete_word(self):
        """Remove word from dictionary"""
        word = self.__get_word()
        if word:
            try:
                del self.__dictionary[word]
                self.__ovewrite_dictionary()
                self.__status_bar.overwrite(word + " - deleted")
            except KeyError:
                self.__status_bar.overwrite("There is no '" + word + "' in the dictionary")
        else:
            self.__status_bar.overwrite("Please enter the word")

def main():
    """Configure the application and start it"""
    root = Application(geometry = "449x120", title = "My own dictionary 2.0")
    word_input = EntryField(root)
    word_input.show(row = 0, column = 0)

    explanation = TextBox(root, width = 40, height = 5, wrap = "word")
    explanation.show(row = 0, column = 1, rowspan = 5)

    status_bar = Inscription(root, text = "Ready to go!")
    status_bar.show(row = 6, column = 1, columnspan = 6, sticky = "E, S")
    
    operations = Handling(file_name = "lib/dict.csv",
                          word_input = word_input,
                          explanation = explanation,
                          status_bar = status_bar)
        
    buttons = {"Find word" : operations.find_word,
               "Add word" : operations.add_word,
               "Delete word" : operations.delete_word}
    root.create_stack_of_buttons(buttons, first_row = 1, column = 0)
    
    root.mainloop()

main()
