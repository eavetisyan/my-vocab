import csv
from abc import (
    ABCMeta,
)


KEY_WORD = 'Word'
KEY_MEANING = 'Meaning'
KEY_EXAMPLE = 'Example'
KEY_SCORE_WORD = 'Guessed with word'
KEY_SCORE_MEANING = 'Guessed with meaning'

FIELD_NAMES = [
    KEY_WORD,
    KEY_MEANING,
    KEY_EXAMPLE,
    KEY_SCORE_WORD,
    KEY_SCORE_MEANING,
]


def get_file_contents(file_path):
    """
    Returns file's contents as a list of dicts
    """

    file_contents = []

    with open(file_path, 'r') as file:

        for line in csv.DictReader(file):
            file_contents.append(line)

    return file_contents


def set_file_contents(file_path, contents):
    """
    Replaces file contents with a list of dicts specified
    """

    with open(file_path, 'w') as file:

        csv_writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        csv_writer.writeheader()
        csv_writer.writerows(contents)


def get_word_row(
    word,
    meaning,
    example,
    guessed_with_word=0,
    guessed_with_meaning=0,
):
    """
    Constructs dict from separated elements
    """
    return {
        KEY_WORD: word,
        KEY_MEANING: meaning,
        KEY_EXAMPLE: example,
        KEY_SCORE_WORD: str(guessed_with_word),
        KEY_SCORE_MEANING: str(guessed_with_meaning),
    }


class Word:
    """
    Word's properties manager
    """

    def __init__(
        self,
        **kwargs,
    ):
        self.word = kwargs.get(KEY_WORD)
        if not self.word:
            raise ValueError('Word is not filled')

        self.meaning = kwargs.get(KEY_MEANING)
        if not self.meaning:
            raise ValueError('Meaning is not filled')

        self.example = kwargs.get(KEY_EXAMPLE)
        self.guessed_with_word = int(kwargs.get(KEY_SCORE_WORD))
        self.guessed_with_meaning = int(kwargs.get(KEY_SCORE_MEANING))

    def set_meaning(
        self,
        meaning,
    ):
        self.meaning = meaning
        self.guessed_with_word = 0
        self.guessed_with_meaning = 0

    def set_example(
        self,
        example,
    ):
        self.example = example

    def increase_guessed_with_word_score(self):
        self.guessed_with_word += 1

    def decrease_guessed_with_word_score(self):
        self.guessed_with_word = max(self.guessed_with_word-1, 0)

    def increase_guessed_with_meaning_score(self):
        self.guessed_with_meaning += 1

    def decrease_guessed_with_meaning_score(self):
        self.guessed_with_meaning = max(self.guessed_with_meaning-1, 0)

    def get_row(self) -> dict:
        return get_word_row(
            self.word,
            self.meaning,
            self.example,
            self.guessed_with_word,
            self.guessed_with_meaning,
        )


class DictionaryContents:
    """
    CSV dictionary manager
    """

    file_contents = []

    def __init__(
        self,
        file_path,
    ):
        self.file_path = file_path

    def get_word(
        self,
        word: str,
    ) -> Word:

        word_row, _ = self._find_row_by_word(word)
        return Word(**word_row)

    def add_word(
        self,
        word_entity: Word,
    ):
        try:
            self._find_row_by_word(word_entity.word)
        except KeyError:
            self.file_contents.append(word_entity.get_row())
            self._write_file()
            return

        raise KeyError(f'{word_entity.word} already exists! Will not overwritten')

    def edit_word(
        self,
        word_entity,
    ):
        _, idx = self._find_row_by_word(word_entity.word)
        self.file_contents[idx] = word_entity.get_row()
        self._write_file()

    def delete_word(
        self,
        word: str,
    ):
        word_row, idx = self._find_row_by_word(word)
        word_entity = Word(**word_row)

        del self.file_contents[idx]
        self._write_file()

        return word_entity

    def save_word(
        self,
        word_entity: Word,
    ):
        try:
            _, idx = self._find_row_by_word(word_entity.word)
            self.file_contents[idx] = word_entity.get_row()

        except KeyError:
            self.file_contents.append(word_entity.get_row())

        self._write_file()

    def _find_row_by_word(
        self,
        word_to_find: str,
    ) -> (dict, int):

        if not self.file_contents:
            self._read_file()

        for idx, word_row in enumerate(self.file_contents):

            if word_row[KEY_WORD].lower() == word_to_find.lower():
                return word_row, idx

        raise KeyError(f'There is no {word_to_find} in the dictionary')

    def _read_file(self):
        self.file_contents = get_file_contents(self.file_path)

    def _write_file(self):
        set_file_contents(
            self.file_path,
            self.file_contents,
        )
