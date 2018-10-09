# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 09:40:15 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Testing application module
Ver 1.3
"""

from itertools import islice
from random import randrange
from re import sub
import csv

WORD = 0
EXPLANATION = 1
GUESS = 2

ID = 1
COUNTER = 0

class Handling():
    """Dictionary management procedures"""
    def __init__(self, file_name, supposition, explanation, status_bar, question):
        """Get dictionary from CSV-file"""
        self.__file_name = file_name
        self.__supposition = supposition
        self.__explanation = explanation
        self.__status_bar = status_bar
        with open(file_name, "r") as file:                                                                                      # Open file for reading just for copying stats and dictionary to RAM
            readed_csv = csv.reader(file)
            self.__read_thru_n_strings(readed_csv, n = 0)                                                                       # Cut off the header
            self.__id = list()
            self.__dictionary = dict()
            for i, line in enumerate(readed_csv):
                self.__id.append([int(line[GUESS]), i])                                                                         # Create id list which contains guesses and words ids
                self.__dictionary[i] = (line[WORD], line[EXPLANATION])                                                          # and create a dictionary with ids as keys and lists of words and explanations as values
        self.__question = question
        self.__dictionary_length = len(self.__dictionary)
        self.__lower_bound = self.__dictionary_length - 1 - self.__dictionary_length // 3                                       # Boundary is a last third of the dictionary
        self.__id.sort(reverse = True)                                                                                          # Sort IDs by descending order
        self.__get_task(self.__lower_bound, self.__dictionary_length)
    
    def __read_thru_n_strings(self, iterable_object, n):
        """Jump from current line to n-distance"""
        return next(islice(iterable_object, n, None))
    
    def __ovewrite_dictionary(self):
        """Overwriting an existing dictionary"""
        header = ["Word", "Explanation", "Guess"]                                                                               # Dictionary heade which were cutted off during the opening CSV-file
        with open(self.__file_name, "w") as file:
            csv_file = csv.writer(file, delimiter = ",", lineterminator = "\n")
            csv_file.writerow(header)                                                                                           # Write headers and stats to CSV
            for line in self.__id:
                word_guess, word_id = line
                row = self.__dictionary[word_id][WORD], self.__dictionary[word_id][EXPLANATION], word_guess
                csv_file.writerow(row)                                                                                          # Write dictionary to CSV
    
    def __get_task(self, lower_bound, upper_bound):
        """Select the word from the dictionary"""
        if self.__dictionary:
            self.__choice = randrange(lower_bound, upper_bound)                                                                 # Get the word from the end of IDs
            self.__task_id = self.__id[self.__choice][ID]
            task = self.__dictionary[self.__task_id]
            self.__question.overwrite(task[WORD])
    
    def implement_an_answer(self):
        """One round of the test"""
        if self.__dictionary:
            user_answers = self.__split_data(self.__supposition.get())
            task = self.__dictionary[self.__task_id]
            correct_answers = self.__split_data(task[EXPLANATION])
            self.__supposition.overwrite("")
            self.__explanation.overwrite(task[WORD] + ":\n" + task[EXPLANATION])
            is_correct = False
            for answer in user_answers:                                                                                         # Checking for the right answer
                for correct in correct_answers:
                    if answer in correct:
                        is_correct = True
                        break
            if is_correct == True:
                self.__status_bar.overwrite(task[WORD] + " - you're right!")
                self.__id[self.__choice][COUNTER] += 1
                self.__id.sort(reverse = True)
                self.__ovewrite_dictionary()
            else:
                self.__status_bar.overwrite("Nope")
            self.__get_task(self.__lower_bound, self.__dictionary_length)
        else:
            self.__status_bar.overwrite("The dictionary is empty!")
    
    def __split_data(self, string):
        """Represent any string as list of words no less than 3 letters"""
        string = string.lower()
        string = sub(r" - ", " ", string)                                                                                       # Remove dashes
        string = sub(r"т\.\w\.", "", string)                                                                                    # Remove abbreviations
        string = sub(r"\b\w{1,3}\b", "", string)                                                                                # Remove prepositions (words less than 3 letters)
        string = sub(r"[\.,;<>\"?/\\!\n_\(\)]", " ", string)                                                                    # Replace symbols with spaces
        string = sub(r"[a-zA-z]", "", string)                                                                                   # Remove Latin alphabet
        return string.split()                                                                                                   # Split words by space
    
if __name__ == "__main__":
    input("Please do not run this file. It's just a library")
