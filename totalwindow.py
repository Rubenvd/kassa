import Tkinter as tk
import tkFont

class TotalWindow:
    def __init__(self, parentwindow, number):
        self.__window = tk.Toplevel(parentwindow)
        self.__window.attributes('-topmost', 'true')
        self.__window.attributes('-fullscreen', 'true')

        self.__window.title("Total")
        self.myfont = tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD)
        numberlabel = tk.Label(self.__window, text="Totaal bedrag: " + str(number),
                        width=20, height=10, font=self.myfont, anchor="center")
        numberlabel.grid(row=0, column=0, sticky="nsew")

        button_ok = tk.Button(self.__window, text="OK", command=self.__okay, anchor="center",height=4,
                              font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD))

        button_ok.grid(row=1, column=0, sticky="nsew")

        self.__window.wait_window()

    def __okay(self):
        self.__window.destroy()