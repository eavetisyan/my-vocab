from abc import ABCMeta, abstractmethod
from tkinter import (
    Tk,
    Button,
    Entry,
    Label,
    NORMAL,
    DISABLED,
    END,
    INSERT,
    LEFT,
)
from tkinter.scrolledtext import ScrolledText


TITLE_BASE = 'My Vocab'

PARAM_HEIGHT = 'height'
PARAM_WIDTH = 'width'

GREETING_GUI_BUTTON_SIZE = {
    PARAM_HEIGHT: 5,
    PARAM_WIDTH: 35,
}

GUI_ID_MAINTENANCE = 1
GUI_ID_TESTING_BY_MEANING = 2
GUI_ID_TESTING_BY_WORD = 3

BUTTON_TXT_FIND = 'Find'
BUTTON_TXT_ADD = 'Add'
BUTTON_TXT_EDIT = 'Edit'
BUTTON_TXT_REMOVE = 'Remove'
BUTTON_TXT_ANSWER = 'Give an Answer!'

LABEL_TXT_WORD = 'Word'
LABEL_TXT_MEANING = 'Meaning'
LABEL_TXT_EXAMPLE = 'Example'


def kill_greeting_gui_and_open_gui_selected(
    greeting_window,
    application_entity,
    gui_id,
):

    def _killer_n_opener():
        greeting_window.destroy()
        application_entity.open_gui_selected(gui_id)

    return _killer_n_opener


def get_greeting_gui(application_entity):
    w = Tk()

    b1 = Button(
        w,
        text='Maintain Your Dictionary',
        command=kill_greeting_gui_and_open_gui_selected(
            w,
            application_entity,
            GUI_ID_MAINTENANCE,
        ),
        **GREETING_GUI_BUTTON_SIZE,
    )
    b1.grid(column=0, row=0)

    b2 = Button(
        w,
        text='Test: Guess The Words With Their Meanings',
        command=kill_greeting_gui_and_open_gui_selected(
            w,
            application_entity,
            GUI_ID_TESTING_BY_MEANING,
        ),
        **GREETING_GUI_BUTTON_SIZE,
    )
    b2.grid(column=1, row=0)

    b3 = Button(
        w,
        text='Test: Describe The Words (beta)',
        command=kill_greeting_gui_and_open_gui_selected(
            w,
            application_entity,
            GUI_ID_TESTING_BY_WORD,
        ),
        **GREETING_GUI_BUTTON_SIZE,
    )
    b3.grid(column=2, row=0)

    w.title(TITLE_BASE)
    w.geometry('765x86')
    w.resizable(False, False)

    return w


class GuiAbstract(metaclass=ABCMeta):

    application_entity = None
    tk_window = None
    word = None
    meaning = None
    label = None

    def __init__(
        self,
        application_entity,
    ):
        self.application_entity = application_entity
        self.tk_window = Tk()

    def get_window(self):
        return self.tk_window

    def set_label(
        self,
        value,
    ):
        self.label.configure(text=value)

    @abstractmethod
    def fill(self):
        pass

    def set_meaning(
        self,
        value,
    ):
        self.meaning.configure(state=NORMAL)
        self.meaning.delete(1.0, END)
        self.meaning.insert(INSERT, value)

    def set_word(
        self,
        value,
    ):
        self.word.configure(state=NORMAL)
        self.word.delete(0, END)
        self.word.insert(0, value)


class GuiMaintenance(GuiAbstract):

    example = None

    def __init__(
        self,
        application_entity,
    ):
        super().__init__(application_entity)
        self.tk_window.title(TITLE_BASE+': Maintain Your Dictionary')
        self.tk_window.geometry('975x190')
        self.tk_window.resizable(False, False)

        Label(
            self.tk_window,
            text=LABEL_TXT_WORD,
            justify=LEFT,
        ).place(x=130, y=0)

        self.word = Entry(
            self.tk_window,
            width=128,
        )
        self.word.place(x=200, y=0)

        Label(
            self.tk_window,
            text=LABEL_TXT_MEANING,
        ).place(x=130, y=45)

        self.meaning = ScrolledText(
            self.tk_window,
            width=94,
            height=4,
        )
        self.meaning.place(x=200, y=22)

        Label(
            self.tk_window,
            text=LABEL_TXT_EXAMPLE,
        ).place(x=130, y=113)

        self.example = ScrolledText(
            self.tk_window,
            width=94,
            height=4,
        )
        self.example.place(x=200, y=94)

        self.label = Label(
            self.tk_window,
            width=240,
            anchor='nw',
        )
        self.label.place(x=0, y=165)

        Button(
            self.tk_window,
            text=BUTTON_TXT_FIND,
            width=15,
            height=2,
            command=application_entity.find_word,
        ).place(x=0, y=0)

        Button(
            self.tk_window,
            text=BUTTON_TXT_ADD,
            width=15,
            height=2,
            command=application_entity.add_word,
        ).place(x=0, y=40)

        Button(
            self.tk_window,
            text=BUTTON_TXT_EDIT,
            width=15,
            height=2,
            command=application_entity.edit_word,
        ).place(x=0, y=80)

        Button(
            self.tk_window,
            text=BUTTON_TXT_REMOVE,
            width=15,
            height=2,
            command=application_entity.delete_word,
        ).place(x=0, y=120)

    def fill(self):
        self.set_label('Ready to Go!')

    def set_example(
        self,
        value,
    ):
        self.example.configure(state=NORMAL)
        self.example.delete(0.0, END)
        self.example.insert(0.0, value)


class GuiTestingAbstract(GuiAbstract, metaclass=ABCMeta):

    def __init__(
        self,
        application_entity,
    ):
        super().__init__(application_entity)
        self.tk_window.geometry('654x570')
        self.tk_window.bind(
            '<Return>',
            lambda _: application_entity.process_answer(),
        )

        self.meaning = ScrolledText(
            self.tk_window,
            width=79,
            height=20,
        )

        self.word = Entry(
            self.tk_window,
            width=108,
        )

        Button(
            self.tk_window,
            text=BUTTON_TXT_ANSWER,
            width=92,
            height=1,
            command=application_entity.process_answer,
        ).grid(column=0, row=2)

        self.label = Label(
            self.tk_window,
            justify=LEFT,
        )
        self.label.grid(column=0, row=3, sticky='W, S')

    @abstractmethod
    def get_answer(self):
        pass


class GuiTestingByMeaning(GuiTestingAbstract):
    def __init__(
        self,
        application_entity,
    ):
        super().__init__(application_entity)
        self.tk_window.title(TITLE_BASE+": Test - Guess The Word Using It's Meaning")

        self.meaning.grid(column=0, row=0)
        self.meaning.configure(state=DISABLED)

        self.word.grid(column=0, row=1)

        self.set_label('Enter the word (or phrase) which is described in the top area')

    def set_meaning(
        self,
        value,
    ):
        super().set_meaning(value)
        self.meaning.configure(state=DISABLED)

    def fill(self):
        word_entity = self.application_entity.get_random_word()
        self.set_meaning(word_entity.meaning)
        self.set_word('')

    def get_answer(self):
        return self.word.get().strip()


class GuiTestingByWord(GuiTestingAbstract):
    def __init__(
        self,
        application_entity,
    ):
        super().__init__(application_entity)
        self.tk_window.title(TITLE_BASE+": Test - Guess The Word Using It's Meaning")

        self.word.grid(column=0, row=0)
        self.word.configure(state=DISABLED)

        self.meaning.grid(column=0, row=1)

        self.set_label('Enter the meaning of the word shown')

    def set_word(
        self,
        value,
    ):
        super().set_word(value)
        self.word.configure(state=DISABLED)

    def fill(self):
        word_entity = self.application_entity.get_random_word()
        self.set_word(word_entity.word)
        self.set_meaning('')

    def get_answer(self):
        return self.meaning.get(0.0, END).strip()
