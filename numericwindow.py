import Tkinter as tk
import tkFont


class NumericWindow:
    def __init__(self, parentwindow):
        self.__window = tk.Toplevel(parentwindow)
        self.__window.attributes('-topmost', 'true')
        self.__window.attributes('-fullscreen', 'true')

        self.__window.title("Numeric input")
        self.__columns = 3
        self.__entrycount = 0
        self.totalNumber = tk.IntVar()

        self.__setup_window_ui(self.__window)

        self.__window.wait_window()

    def get_value(self):
        return self.totalNumber.get()

    def __setup_window_ui(self, window):
        label_total = tk.Label(window, textvariable=self.totalNumber, height=3,
                               font=tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD))
        label_total.grid(row=0, column=0, columnspan=3)

        self.__add_button(self.__create_number(self.__window, 1))
        self.__add_button(self.__create_number(self.__window, 2))
        self.__add_button(self.__create_number(self.__window, 3))
        self.__add_button(self.__create_number(self.__window, 4))
        self.__add_button(self.__create_number(self.__window, 5))
        self.__add_button(self.__create_number(self.__window, 6))
        self.__add_button(self.__create_number(self.__window, 7))
        self.__add_button(self.__create_number(self.__window, 8))
        self.__add_button(self.__create_number(self.__window, 9))
        self.__add_button(self.__create_number(self.__window, 0))

        button_clear = tk.Button(window, text="RESET", command= self.__reset,
                                 font=tkFont.Font(family='Helvetica', size=18, weight=tkFont.BOLD))
        self.__add_button(button_clear)

        button_ok = tk.Button(window, text="OK", command=self.__close,
                              font=tkFont.Font(family='Helvetica', size=18, weight=tkFont.BOLD))
        self.__add_button(button_ok)

    def __close(self):
        self.__window.destroy()

    def __reset(self):
        self.totalNumber.set(0)

    def __create_number(self, window, number):
        return tk.Button(window, text=number, command=lambda: self.__adder(number))

    def __adder(self, number):
        self.totalNumber.set(self.totalNumber.get() * 10 + number)

    def __add_button(self, button):
        helv36 = tkFont.Font(family='Helvetica', size=28)
        button.config(height=3, width=10, font=helv36)
        button.grid(row=(1 + self.__entrycount / self.__columns),
                    column=(self.__entrycount % self.__columns))
        self.__entrycount += 1