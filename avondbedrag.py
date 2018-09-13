import Tkinter as tk
import tkFont

class AvondBedrag:
    def __init__(self, parentwindow, number):
        self.einde = False
        self.__window = tk.Toplevel(parentwindow)
        self.__window.attributes('-topmost', 'true')
        self.__window.attributes('-fullscreen', 'true')

        self.__window.title("Total")
        self.myfont = tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD)
        numberlabel = tk.Label(self.__window, text="Totaal bedrag: " + str(number),
                        width=40, height=10, font=self.myfont, anchor="center")
        numberlabel.grid(row=0, column=0, sticky="nsew", columnspan=2)

        button_ok = tk.Button(self.__window, text="Terug", command=self.__okay, anchor="center",height=4,
                              font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD))

        button_ok.grid(row=1, column=0, sticky="nsew")

        button_ok = tk.Button(self.__window, text="Einde avond", command=self.__einde_avond, anchor="center", height=4,
                              font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD))

        button_ok.grid(row=1, column=1, sticky="nsew")

        self.__window.wait_window()

    def __okay(self):
        self.__window.destroy()

    def __einde_avond(self):
        self.einde = True
        self.__window.destroy()

    def einde(self):
        return self.einde