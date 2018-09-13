import Tkinter as tk
import tkFont

class MessageWindow:
    def __init__(self, parentwindow, message):
        self.__window = tk.Toplevel(parentwindow)
        self.__window.attributes('-topmost', 'true')
        self.__window.attributes('-fullscreen', 'true')

        self.__window.title("Total")
        numberlabel = tk.Label(self.__window, text=message, width=40, height=10, anchor="center")
        numberlabel.grid(row=0, column=0, sticky="nsew")

        button_ok = tk.Button(self.__window, text="OK", command=self.__okay, anchor="center",height=4)

        button_ok.grid(row=1, column=0, sticky="nsew")

        self.__window.wait_window()

    def __okay(self):
        self.__window.destroy()