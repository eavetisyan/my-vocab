# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 12:09:43 2018

@author: Eduard Avetisyan (ed.avetisyan95@gmail.com)
----------------
Application that allows you to create and fill your own dictionary
Ver 1.1
"""

from modules.gui import *
import shelve

class DictApp(Application):
    """Subclass of Application which opens an external file"""
    def __init__(self, title, geometry, file_name, resizable = False):
        """Open dictionary file before starting application"""
        super().__init__(title, geometry, resizable)
        self.__dictionary = shelve.open(file_name)

    def dictionary(self):
        """Get dictionary handle"""
        return self.__dictionary

    def __exit__(self):
        """Close file and exit program"""
        self.dictionary.close()
        super().__exit__()

class Handling():
    """Dictionary management procedures"""
    def __init__(self, dictionary, word_input, explanation, status_bar):
        self.dictionary = dictionary
        self.word_input = word_input
        self.explanation = explanation
        self.status_bar = status_bar
    
    def __get_word(self):
        """Pop the word from text entry and set the first letter to upper case"""
        word = self.word_input.get()
        if word:
            word = word[0].upper() + word[1:] # This is because the text entry may contains more than one word
        return word
    
    def find_word(self):
        """Finding word function"""
        word = self.__get_word()
        if word:
            try:
                self.explanation.overwrite(self.dictionary[word])
            except KeyError:
                self.status_bar.overwrite("There is no '" + word + "' in the dictionary")
        else:
            self.status_bar.overwrite("Please enter the word")

    def add_word(self):
        """Add word to dictionary"""
        word = self.__get_word()
        if word:
            self.dictionary[word] = self.explanation.get('0.0', 'end')
            self.dictionary.sync()
            self.status_bar.overwrite(word + " - added to dictionary")
        else:
            self.status_bar.overwrite("Please enter the word")

    def delete_word(self):
        """Remove word from dictionary"""
        word = self.__get_word()
        if word:
            try:
                del self.dictionary[word]
                self.status_bar.overwrite(word + " - deleted")
                self.dictionary.sync()
            except KeyError:
                self.status_bar.overwrite("There is no '" + word + "' in the dictionary")
        else:
            self.status_bar.overwrite("Please enter the word")

def main():
    """Configure the application and start it"""
    root = DictApp(geometry = "449x120", title = "My own dictionary", file_name = "lib/dict")
    word_input = EntryField(root)
    word_input.show(row = 0, column = 0)

    explanation = TextBox(root, width = 40, height = 5, wrap = "word")
    explanation.show(row = 0, column = 1, rowspan = 5)

    status_bar = Inscription(root, text = "Ready to go!")
    status_bar.show(row = 6, column = 1, columnspan = 6, sticky = "E, S")
    
    operations = Handling(dictionary = root.dictionary(),
                          word_input = word_input,
                          explanation = explanation,
                          status_bar = status_bar)
        
    buttons = {"Find word" : operations.find_word,
               "Add word" : operations.add_word,
               "Delete word" : operations.delete_word}
    root.create_stack_of_buttons(buttons, first_row = 1, column = 0)
    
    root.mainloop()

main()
