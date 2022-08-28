try:
    import random
    import json
    import PySimpleGUI as sg
    import re
except Exception as error:
    print(error)


class Wordle:
    def __init__(self):
        # Settings
        self.random_word = str(random.choice(open("words").read().splitlines()))
        self.current_row = 0
        self.tries = 4
        self.width, self.height = 1060, 900
        self.font, self.input_font = ("Arial", 25), ("Arial", 30)
        self.background_color, self.button_color = "#8697e3", "#1f164a"
        self.red, self.yellow, self.green = "#cc2d2d", "#e8e348", "#2dd128"
        self.guesses = []

        self.wordle_5_words = [
            [
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r1k1"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r1k2"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r1k3"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r1k4"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r1k5")
            ],
            [
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r2k1"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r2k2"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r2k3"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r2k4"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r2k5")
            ],
            [
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r3k1"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r3k2"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r3k3"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r3k4"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r3k5")
            ],
            [
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r4k1"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r4k2"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r4k3"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r4k4"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r4k5")
            ],
            [
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r5k1"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r5k2"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r5k3"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r5k4"),
                sg.Text("[ x ]", pad=(4, 10), font=self.font, key="r5k5")
            ]
        ]

        self.input_field = sg.Input(
            key="-INPUT-",
            do_not_clear=False,
            size=(5, 1),
            border_width=1,
            pad=(270, 10),
            font=self.input_font
        )
        self.tries_text = sg.Text(
            f"Tries: {self.tries}",
            key="-tries-",
            background_color=self.background_color,
            pad=(265, 10),
            font=self.font
        )

        quit_button = sg.Button(
            "Leave",
            key="-quit-",
            size=(10, 3),
            auto_size_button=True,
            button_color=self.button_color,
            pad=(250, 10),
            font=self.font
        )

        restart_button = sg.Button(
            "Restart",
            key="-restart-",
            size=(10, 3),
            auto_size_button=True,
            button_color=self.button_color,
            pad=(250, 10),
            font=self.font
        )

        self.gui_text = [
            [self.input_field],
            [self.tries_text],
            [restart_button],
            [quit_button],
        ]

        self.layout = [
            [sg.Column(self.wordle_5_words, background_color=self.background_color)],
            [sg.Column(self.gui_text, background_color=self.background_color)]
        ]
        self.window = sg.Window(
            title=self.random_word,
            layout=self.layout,
            margins=(200, 100),
            size=(self.width, self.height),
            background_color=self.background_color,
            element_justification='centre',
            finalize=True
        )

    def start(self):
        def restart_game(self):
            self.random_word = random.choice(open("words", "r").read().splitlines())
            for i in self.wordle_5_words:
                for j in i:
                    j.update("[ x ]", font=self.font, text_color="#ffffff")
            # Reset every element
            self.tries = 4
            self.current_row = 0
            self.guesses.clear()
            self.window.set_title(self.random_word)
            self.window['-tries-'].update(f"Tries: {self.tries}")
            self.window['-INPUT-'].update(disabled=False)

        self.window["-INPUT-"].bind("<Return>", "_Enter")
        while True:
            if self.tries == -1:
                self.window['-INPUT-'].update(disabled=True)
                self.window['-tries-'].update("You lost!")
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "-quit-":
                break
            if event == "-restart-":
                restart_game(self=self)
            elif event == "-INPUT-" + "_Enter":
                latest_input = values['-INPUT-']

                # If the word typed out is the same as the random word automatically end the game
                if latest_input == self.random_word:
                    for i in range(5):
                        self.wordle_5_words[self.current_row][i].update(
                            f"[ {latest_input[i]} ]", text_color=self.green
                        )
                    self.window['-tries-'].update(f"GG!")
                    self.window['-INPUT-'].update(disabled=True)

                # Otherwise, check if the word contains 5 letters and start comparing
                elif len(latest_input) == 5:
                    self.guesses.append(latest_input)
                    for i in range(5):
                        # Check if the current letter is the same one as the random words
                        if latest_input[i] == self.random_word[i]:
                            self.wordle_5_words[self.current_row][i].update(
                                f"[ {latest_input[i]} ]", text_color=self.green
                            )
                        # Check if the current letter is anywhere in the word
                        elif latest_input[i] in list(self.random_word):
                            self.wordle_5_words[self.current_row][i].update(
                                f"[ {latest_input[i]} ]", text_color=self.yellow
                            )
                        # Otherwise turn the letter into a red character
                        elif latest_input[i] != self.random_word[i]:
                            self.wordle_5_words[self.current_row][i].update(
                                f"[ {latest_input[i]} ]", text_color=self.red
                            )

                    self.tries -= 1
                    self.window["-tries-"].update(f"Tries: {self.tries}")
                    self.current_row += 1
        self.window.close()


if __name__ == '__main__':
    game = Wordle()
    game.start()
