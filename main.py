try:
    import random
    import json
    import PySimpleGUI as sg
except Exception as error:
    print(error)


class Wordle:
    def __init__(self):
        self.random_word = random.choice(open("words").read().splitlines())
        self.tries = 4
        self.guesses = []
        self.tries_text = sg.Text(f"Tries left: {self.tries}", key="-tries-")
        self.gui_text = [
            [sg.Input(key="-INPUT-", do_not_clear=False)],
            [sg.Button("Submit"), sg.Button("Clear")],
            [self.tries_text]
        ]
        self.word_box = sg.Listbox(
            values=[],
            enable_events=True,
            size=(5, 5),
            key="-WORDBOX-",
            no_scrollbar=True
        )
        self.end_game = [[sg.Button("Quit Game", size=(10, 3))]]

        self.layout = [
            [
                sg.Column(self.end_game),
                sg.VSeperator(),
                sg.Column([[self.word_box]]),
                sg.Column(self.gui_text)
            ]
        ]
        self.window = sg.Window(title=self.random_word, layout=self.layout, margins=(100, 50))

    def start(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Quit Game":
                break
            elif event == "Clear":
                self.word_box.update(values=[])
            elif event == "Submit":
                latest_input = values['-INPUT-']
                if latest_input != self.random_word:
                    if self.tries == 0:
                        self.window['-tries-'].update("You lost")
                    self.tries -= 1
                    self.window["-tries-"].update(f"Tries left: {self.tries}")
                    self.guesses.append(latest_input)
                    self.word_box.update(self.guesses)
                else:
                    pass
        self.window.close()


if __name__ == '__main__':
    game = Wordle()
    game.start()
