from lib.common import (
    DictionaryContents,
    Word,
    get_word_row,
)
from lib.testing_engine import (
    DictionaryContentsTestingByMeaning,
    DictionaryContentsTestingByWord,
)
from lib.gui import (
    GUI_ID_MAINTENANCE,
    GUI_ID_TESTING_BY_MEANING,
    GUI_ID_TESTING_BY_WORD,
    get_greeting_gui,
    GuiMaintenance,
    GuiTestingByMeaning,
    GuiTestingByWord,
    END,
)


DICTIONARY_FILE_PATH = 'dictionary.csv'

IDX_GUI_CLS = 0
IDX_DICTIONARY_CONTENTS_CLS = 1

GUI_ID_MAPPING = {
    GUI_ID_MAINTENANCE: (
        GuiMaintenance,
        DictionaryContents,
    ),
    GUI_ID_TESTING_BY_MEANING: (
        GuiTestingByMeaning,
        DictionaryContentsTestingByMeaning,
    ),
    GUI_ID_TESTING_BY_WORD: (
        GuiTestingByWord,
        DictionaryContentsTestingByWord,
    ),
}


class Application:

    gui_entity = None
    dictionary_contents_entity = None
    current_word = None

    def run(self):

        greeting_gui = get_greeting_gui(self)
        greeting_gui.mainloop()

    def open_gui_selected(
        self,
        gui_id,
    ):
        if not gui_id:
            return

        self.dictionary_contents_entity = GUI_ID_MAPPING[gui_id][IDX_DICTIONARY_CONTENTS_CLS](DICTIONARY_FILE_PATH)

        self.gui_entity = GUI_ID_MAPPING[gui_id][IDX_GUI_CLS](self)
        self.gui_entity.fill()
        self.gui_entity.get_window().mainloop()

    def find_word(self):
        try:
            word_entity = self.dictionary_contents_entity.get_word(
                self.gui_entity.word.get().strip()
            )
        except KeyError as e:
            self.gui_entity.set_label(str(e))
            return

        self.gui_entity.set_word(word_entity.word)
        self.gui_entity.set_meaning(word_entity.meaning)
        self.gui_entity.set_example(word_entity.example)

        label_text = word_entity.word + ' - Found!'
        self.gui_entity.set_label(label_text)

    def add_word(self):
        try:
            word_entity = self._get_word_entity_from_gui()
            self.dictionary_contents_entity.add_word(word_entity)
        except (KeyError, ValueError) as e:
            self.gui_entity.set_label(str(e))
            return

        label_text = word_entity.word + ' - Added to Your Dictionary'
        self.gui_entity.set_label(label_text)

    def edit_word(self):
        try:
            word_entity = self._get_word_entity_from_gui()
            self.dictionary_contents_entity.edit_word(word_entity)
        except (KeyError, ValueError) as e:
            self.gui_entity.set_label(str(e))
            return

        label_text = word_entity.word + ' - Edited'
        self.gui_entity.set_label(label_text)

    def delete_word(self):
        try:
            word_entity = self.dictionary_contents_entity.delete_word(
                self.gui_entity.word.get().strip()
            )
        except (KeyError, ValueError) as e:
            self.gui_entity.set_label(str(e))
            return

        self.gui_entity.set_word(word_entity.word)
        self.gui_entity.set_meaning(word_entity.meaning)
        self.gui_entity.set_example(word_entity.example)

        label_text = word_entity.word + ' - Deleted'
        self.gui_entity.set_label(label_text)

    def process_answer(self):
        answer = self.gui_entity.get_answer()

        try:
            answer_is_correct = self.dictionary_contents_entity.check_answer(answer)
        except ValueError as e:
            self.gui_entity.set_label(str(e))
            return

        label_text = ''

        if answer_is_correct:
            label_text += 'Correct!'
        else:
            label_text += 'Nope!'

        word_entity = self.dictionary_contents_entity.current_word

        label_text += '\n'*2 + word_entity.word + ':\n' + word_entity.meaning

        if word_entity.example:
            label_text += '\n'*2 + 'Example: ' + word_entity.example

        self.gui_entity.set_label(label_text)
        self.gui_entity.fill()

    def get_random_word(self):
        return self.dictionary_contents_entity.get_random_word()

    def _get_word_entity_from_gui(self):
        return Word(
            **get_word_row(
                self.gui_entity.word.get().strip(),
                self.gui_entity.meaning.get(0.0, END).strip(),
                self.gui_entity.example.get(0.0, END).strip(),
            )
        )


Application().run()
