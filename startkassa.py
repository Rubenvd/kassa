import Tkinter as tk
from numericwindow import *
from notecount import *
import tkFont


class KassaVuller:

    class Button:
        def __init__(self, note):
            self.notecount = note
            self.var = tk.IntVar()

        def number_input(self,window):
            self.notecount.amount = NumericWindow(window).get_value()
            self.var.set(self.notecount.amount)

    def __init__(self, parentwindow, notecollection):
        self.__notes = notecollection
        self.__money = []

        for note in self.__notes:
            self.__money.append(self.Button(note))

        self.__columnWidth = 4
        self.__entryCount = 0
        self.__window = tk.Toplevel(parentwindow)
        self.__window.attributes('-topmost', 'true')
        self.__window.title("KassaVuller")

        self.__setup_window_ui(self.__window)
        self.__window.wait_window()

    def get_value(self):
        return self.__notes

    def __okay(self):
        self.__window.destroy()

    def __setup_window_ui(self, window):
        for number in self.__money:
            self.__add_money_unit(window, number)

        button_ok = tk.Button(window, text="OK", command=self.__okay, anchor="center",
                              font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD))

        button_ok.grid(row=self.__entryCount, column=0, columnspan=2, sticky=("N", "S", "E", "W"))

    def __add_money_unit(self, window, number):
        label_total = tk.Label(window, text="Amount of " + str(number.notecount.note) + ": ", width=18,
                               font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD),
                               anchor="w")
        label_total.grid(row=self.__entryCount,
                         column=0)

        button_total = tk.Button(window, textvariable=number.var, width=4,
                                 command=lambda: number.number_input(self.__window),
                                 font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD))
        button_total.grid(row=self.__entryCount,
                          column=1)

        self.__entryCount += 1