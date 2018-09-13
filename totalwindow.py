import Tkinter as tk

class TotalWindow:
    def __init__(self, parentwindow, number):
        self.agreed = False
        self.__window = tk.Toplevel(parentwindow)
        self.__window.attributes('-topmost', 'true')
        self.__window.attributes('-fullscreen', 'true')

        self.__window.title("Total")
        numberlabel = tk.Label(self.__window, text="Totaal bedrag: " + str(number),
                        width=20, height=10, anchor="center")
        numberlabel.grid(row=0, column=0, columnspan=2, sticky="nsew")

        button_ok = tk.Button(self.__window, text="Akkoord", command=self.__okay, anchor="center", height=6, width=10)
        button_cancel = tk.Button(self.__window, text="Terug", command=self.__cancel, anchor="center", height=6, width=10)

        button_cancel.grid(row=1, column=0, sticky="nsew")
        button_ok.grid(row=1, column=1, sticky="nsew")

        self.__window.wait_window()

    def __okay(self):
        self.agreed = True
        self.__window.destroy()

    def __cancel(self):
        self.agreed = False
        self.__window.destroy()

    def has_agreed(self):
        return self.agreed
