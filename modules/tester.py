# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 09:40:15 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Testing application module
Ver 1.5
"""

from random import randrange
from operator import itemgetter
from re import sub
import csv

WORD = 1
GUESS = 0

class Handling():
    """Dictionary management procedures"""
    def __init__(self, file_name, supposition, explanation_box, status_bar, question):
        """Get dictionary from CSV-file"""
        self.__file_name = file_name
        self.__supposition = supposition
        self.__explanation = explanation_box
        self.__status_bar = status_bar
        self.__question = question
        with open(file_name, "r") as file:                                                                                      # Open file for reading just for copying stats and dictionary to RAM
            readed_csv = csv.reader(file)
            next(readed_csv)                                                                                                    # Cut off the header
            self.__words = list()
            self.__explanation_of = dict()
            for word, explanation, guess in readed_csv:
                self.__words.append([int(guess), word])                                                                         # Create words list which contains lists of [guess, word] values
                self.__explanation_of[word] = explanation                                                                       # and create a dictionary with words as keys and explanations as values
        self.__dictionary_length = len(self.__explanation_of)
        self.__lower_bound = self.__dictionary_length - 1 - self.__dictionary_length // 3                                       # The boundary is a last third of the dictionary
        self.__words.sort(reverse = True)                                                                                       # Sort words by descending order of guesses
        self.__get_task(self.__lower_bound, self.__dictionary_length, previous_task = None)
        
    def __ovewrite_dictionary(self):
        """Overwriting an existing dictionary"""
        header = ["Word", "Explanation", "Guess"]                                                                               # Dictionary heade which were cutted off during the opening CSV-file
        with open(self.__file_name, "w") as file:
            csv_file = csv.writer(file, delimiter = ",", lineterminator = "\n")
            csv_file.writerow(header)                                                                                           # Write headers and stats to CSV
            for guess, word in sorted(self.__words, key = itemgetter(WORD)):
                row = word, self.__explanation_of[word], guess
                csv_file.writerow(row)                                                                                          # Write dictionary to CSV
    
    def __get_task(self, lower_bound, upper_bound, previous_task):
        """Select the word from the dictionary"""
        if upper_bound is not 0:
            while True:
                self.__choice = randrange(lower_bound, upper_bound)                                                             # Get the word from the end of __words
                self.__task = self.__words[self.__choice][WORD]
                if previous_task != self.__task:
                    break
            self.__question.overwrite(self.__task)
    
    def implement_an_answer(self):
        """One round of the test"""
        if not self.__explanation_of:
            self.__status_bar.overwrite("The dictionary is empty!")
        else:
            user_answers = self.__split_data(self.__supposition.get())
            correct_answers = self.__split_data(self.__explanation_of[self.__task])
            self.__supposition.overwrite("")
            self.__explanation.overwrite(self.__task + ":\n" + self.__explanation_of[self.__task])
            is_correct = False
            for answer in user_answers:                                                                                         # Checking for the right answer
                for correct in correct_answers:
                    if answer in correct:
                        is_correct = True
                        break
            if is_correct == True:
                self.__status_bar.overwrite(self.__task + " - you're right!")
                self.__words[self.__choice][GUESS] += 2
                self.__words.sort(reverse = True)
                self.__ovewrite_dictionary()
            else:
                if self.__words[self.__choice][GUESS] > 0:                                                                    # Decrease the guess GUESS if it is above zero
                    self.__words[self.__choice][GUESS] -= 1
                self.__status_bar.overwrite("Nope")
            self.__get_task(self.__lower_bound, self.__dictionary_length, self.__task)
    
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
