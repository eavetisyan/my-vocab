# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:27:13 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Module for handling of dictionary
Ver 1.0
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
            stats = self.__read_thru_n_strings(readed_csv)                                                                      # Jump to the stats 
            self.__max_guess, self.__min_guess, self.__max_count, self.__min_count = map(int, stats)                            # and save them
            self.__read_thru_n_strings(readed_csv)                                                                              # Cut off headers and stats
            self.__dictionary = {line[WORD] : [line[DESCRIPTION], int(line[COUNTER])] for line in readed_csv}                   # Constructing dictionary as "word : [explanation, guess]" items
    
    def __read_thru_n_strings(self, iterable_object, n = 1):
        """Jump from current line to n-distance"""
        return next(islice(iterable_object, n, None))
    
    def __ovewrite_dictionary(self):
        """Overwriting an existing dictionary"""
        stats_header = [["Max guess", "Min guess", "Counter of maximals", "Counter of minimals"]]                               # Headers and stats
        empty_row = [[]]                                                                                                        # which were cutted off
        dictionary_header = [["Word", "Explanation", "Guess"]]                                                                  # during the opening CSV-file
        header = stats_header + [[self.__max_guess, self.__min_guess, self.__max_count, self.__min_count]] + empty_row + dictionary_header
        with open(self.__file_name, "w") as file:
            csv_file = csv.writer(file, delimiter = ",", lineterminator = "\n")
            csv_file.writerows(header)                                                                                          # Write headers and stats to CSV
            for row in self.__dictionary_lines(self.__dictionary):
                csv_file.writerow(row)                                                                                          # Write dictionary to CSV
    
    def __dictionary_lines(self, dicitonary):
        """Get next dictionary line as list"""
        for line in dicitonary.items():
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
    
    def add_word(self, guess = 0):
        """Add word to dictionary"""
        word = self.__get_word()
        if word:
            if word not in self.__dictionary:
                self.__dictionary[word] = [self.__explanation.get('0.0', 'end - 1c'), guess]
                if guess == self.__min_guess:                                                                                   # Update minimal guess if it's equals to the current guess
                    self.__min_guess, self.__min_count = self.__guess_recalculation(self.__dictionary, self.__min_guess, self.__min_count, increase_guess = True, reverse = False)
                    if self.__min_guess == self.__max_guess:                                                                        # Update counter of max gess if max and min values are the same
                        self.__max_count = self.__min_count
                elif guess < self.__min_guess:                                                                                  # Set minimal guess as the current if the first one is above
                    self.__min_guess = guess
                    self.__min_count = 1
                self.__ovewrite_dictionary()
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
                guess = self.__dictionary[word][GUESS]
                self.__dictionary[word] = [self.__explanation.get('0.0', 'end - 1c'), guess]
                self.__ovewrite_dictionary()
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
                guess = self.__dictionary[word][GUESS]
                del self.__dictionary[word]
                if self.__dictionary:                                                                                           # Not empty dictionary case:
                    if guess == self.__max_guess:                                                                                   # Update maximal guess if it's equals to the current guess
                        self.__max_guess, self.__max_count = self.__guess_recalculation(self.__dictionary, self.__max_guess, self.__max_count, increase_guess = False, reverse = True)
                        if self.__max_guess == self.__min_guess:                                                                        # Update counter of min guess if min and max values are the same
                            self.__min_count = self.__max_count
                    elif guess == self.__min_guess:                                                                                 # Update minimal guess if it's equals to the current guess
                        self.__min_guess, self.__min_count = self.__guess_recalculation(self.__dictionary, self.__min_guess, self.__min_count, increase_guess = False, reverse = False)
                        if self.__min_guess == self.__max_guess:                                                                        # Update counter of max guess if max and min values are the same
                            self.__max_count = self.__min_count
                else:                                                                                                           # Empty dictionary case - set stats to zero
                    self.__max_guess = self.__min_guess = 0
                    self.__max_count = self.__min_count = 0
                
                self.__ovewrite_dictionary()
                self.__status_bar.overwrite(word + " - deleted")
            else:
                self.__status_bar.overwrite("There is no '" + word + "' in the dictionary")
        else:
            self.__status_bar.overwrite("Please enter the word")
        
    def __guess_recalculation(self, dictionary, guess, guess_counter, increase_guess, reverse):
        """Update minimal or maximal guess value"""
        if increase_guess == True:                                                                                              # Adding word case
            guess_changing = 1
        else:                                                                                                                   # Removing word case
            guess_changing = -1
        if reverse == False:                                                                                                    # Order by ascending guess values case
            dictionary = self.__sort_dictionary(dictionary, reverse = False)
        guess_counter = guess_counter + guess_changing
        if guess_counter == 0:
            guess = self.__read_thru_n_strings(dictionary.items(), n = 0)[VALUE][GUESS]                                         # Get guess of the first item
            guess_counter = self.__guess_counter(dictionary, guess, reverse = reverse)
        return guess, guess_counter
    
    def __guess_counter(self, dictionary, guess, reverse):
        """Count the quantity of words with 'guess' value"""
        guess_counter = 0
        for line in dictionary.items():
            if line[VALUE][GUESS] == guess:
                guess_counter += 1
            elif reverse is False and line[VALUE][GUESS] > guess:
                break
            elif reverse is True and line[VALUE][GUESS] < guess:
                break
        return guess_counter
    
    def __sort_dictionary(self, dictionary, reverse = True):
        """Sort dictionary items by guess values"""
        return dict(sorted(dictionary.items(), key = lambda value: value[VALUE][GUESS], reverse = reverse))

if __name__ == "__main__":
    input("Please do not run this file. It's just a library!")