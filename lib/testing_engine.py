from random import randrange
from abc import (
    ABCMeta,
    abstractmethod,
)

from .common import (
    DictionaryContents,
    KEY_WORD,
    KEY_SCORE_WORD,
    KEY_SCORE_MEANING,
    Word,
)


TESTING_TYPE_BY_WORD = 'BY_WORD'
TESTING_TYPE_BY_MEANING = 'BY_MEANING'


def get_random_word(
    dictionary_sorted,
    current_word,
):
    file_length = len(dictionary_sorted)

    # We will return the words from the third of the scoreboard which has the minimal scores
    upper_bound = file_length // 3 + 1
    word_selected_idx = randrange(0, upper_bound)

    word_selected_row = dictionary_sorted[word_selected_idx]

    if current_word and upper_bound > 1 and current_word.word == word_selected_row[KEY_WORD]:

        return get_random_word(
            dictionary_sorted,
            current_word,
        )

    return Word(**word_selected_row)


class DictionaryContentsTestingAbstract(DictionaryContents, metaclass=ABCMeta):

    current_word = None

    @property
    @abstractmethod
    def _sort_key(self):
        pass

    def get_random_word(self):

        if not self.file_contents:
            self._read_file()

        self.file_contents.sort(key=lambda d: int(d[self._sort_key]))

        self.current_word = get_random_word(
            self.file_contents,
            self.current_word
        )

        return self.current_word

    def check_answer(
        self,
        answer: str,
    ):
        if len(answer) < 2:
            raise ValueError('The length of the answer is too small')

        answer_is_correct = self._answer_is_correct(answer)

        if answer_is_correct:
            self._increase_score()
        else:
            self._decrease_score()

        self.save_word(self.current_word)

        return answer_is_correct

    def _answer_is_correct(
        self,
        user_answer: str,
    ):
        correct_answer = self._get_correct_answer()
        return user_answer.lower() in correct_answer.lower()

    @abstractmethod
    def _get_correct_answer(self):
        pass

    @abstractmethod
    def _increase_score(self):
        pass

    @abstractmethod
    def _decrease_score(self):
        pass


class DictionaryContentsTestingByMeaning(DictionaryContentsTestingAbstract):

    @property
    def _sort_key(self):
        return KEY_SCORE_MEANING

    def _get_correct_answer(self):
        return self.current_word.word

    def _increase_score(self):
        self.current_word.increase_guessed_with_meaning_score()

    def _decrease_score(self):
        self.current_word.decrease_guessed_with_meaning_score()


class DictionaryContentsTestingByWord(DictionaryContentsTestingAbstract):

    @property
    def _sort_key(self):
        return KEY_SCORE_WORD

    def _get_correct_answer(self):
        return self.current_word.meaning

    def _increase_score(self):
        self.current_word.increase_guessed_with_word_score()

    def _decrease_score(self):
        self.current_word.decrease_guessed_with_word_score()
