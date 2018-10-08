# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 09:39:36 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Dictionary handling module
Ver 3.1
"""

from itertools import islice
import csv

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
            self.__read_thru_n_strings(readed_csv, n = 0)                                                                       # Cut off the header
            self.__dictionary = {line[WORD] : [line[DESCRIPTION], int(line[COUNTER])] for line in readed_csv}                   # Constructing dictionary as "word : [explanation, guess]" items
    
    def __read_thru_n_strings(self, iterable_object, n):
        """Jump from current line to n-distance"""
        return next(islice(iterable_object, n, None))
    
    def __ovewrite_dictionary(self):
        """Overwriting an existing dictionary"""
        header = ["Word", "Explanation", "Guess"]                                                                    # Dictionary heade which were cutted off during the opening CSV-file
        with open(self.__file_name, "w") as file:
            csv_file = csv.writer(file, delimiter = ",", lineterminator = "\n")
            csv_file.writerow(header)                                                                                          # Write headers and stats to CSV
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
        word = word.strip()
        if word:
            if " " in word:
                word = word[0].upper() + word[1:]                                                                               # This is because the text entry may contains more than one word
            else:
                word = word.capitalize()                                                                                        # Case for a single word
        return word
    
    def find_word(self):
        """Finding word function"""
        word = self.__get_word()
        if word:
            if word in self.__dictionary:
                self.__explanation.overwrite(self.__dictionary[word][EXPLANATION])
                self.__status_bar.overwrite(word + " - found!")
            else:
                self.__status_bar.overwrite("There is no '" + word + "' in the dictionary")
        else:
            self.__status_bar.overwrite("Please enter the word")
    
    def add_word(self):
        """Add word to dictionary"""
        word = self.__get_word()
        if word:
            if word not in self.__dictionary:
                self.__set_dictionary_item(word, guess = 0)
                self.__status_bar.overwrite(word + " - added to dictionary")
            else:
                self.__status_bar.overwrite("This word is already exists!")
        else:
            self.__status_bar.overwrite("Please enter the word")
    
    def edit_word(self):
        """Change the explanation of an existing word"""
        word = self.__get_word()
        if word:
            if word in self.__dictionary:
                self.__set_dictionary_item(word, guess = self.__dictionary[word][GUESS])
                self.__status_bar.overwrite(word + " - explanation edited")
            else:
                self.__status_bar.overwrite("There is no '" + word + "' in the dictionary")
        else:
            self.__status_bar.overwrite("Please enter the word")
    
    def delete_word(self):
        """Remove word from dictionary"""
        word = self.__get_word()
        if word:
            if word in self.__dictionary:
                self.__explanation.overwrite(self.__dictionary[word][EXPLANATION])
                del self.__dictionary[word]
                self.__ovewrite_dictionary()
                self.__status_bar.overwrite(word + " - deleted")
            else:
                self.__status_bar.overwrite("There is no '" + word + "' in the dictionary")
        else:
            self.__status_bar.overwrite("Please enter the word")
    
    def __set_dictionary_item(self, word, guess):
        self.__dictionary[word] = [self.__explanation.get('0.0', 'end - 1c'), guess]
        self.__ovewrite_dictionary()
    
    def __sort_dictionary(self, dictionary, reverse = True):
        """Sort dictionary items by guess values"""
        return dict(sorted(dictionary.items(), key = lambda value: value[VALUE][GUESS], reverse = reverse))
    
if __name__ == "__main__":
    input("Please do not run this file. It's just a library")