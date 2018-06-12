import Tkinter as tk
import tkFont
from numericwindow import *
from startkassa import *
from notecount import *
from bestelling import *


class KassaSysteem:

    class eenheidBestelling:
        def __init__(self, bestelling):
            self.tk_amount = tk.IntVar()
            self.bestelling = bestelling

        def plus_one(self):
            self.bestelling.amount += 1
            self.tk_amount.set(self.bestelling.amount)

        def eindbedrag(self):
            return self.bestelling.bedrag * self.bestelling.amount

        def reset(self):
            self.bestelling.amount = 0
            self.tk_amount.set(self.bestelling.amount)

    def __init__(self):
        self.notecollection = [ NoteCount(50, 0),
                                NoteCount(20, 0),
                                NoteCount(10, 0),
                                NoteCount(5, 0),
                                NoteCount(2, 0),
                                NoteCount(1, 0),
                                NoteCount(0.5, 0),
                                NoteCount(0.2, 0),
                                NoteCount(0.1, 0)]
        self.huidige_rekening = {}
        self.rootWindow = tk.Tk()
        #self.rootWindow.attributes("-fullscreen", True)
        self.rootWindow.grid_columnconfigure(0, weight=1)
        self.rootWindow.grid_rowconfigure(0, weight=1)
        self.rootWindow.grid_columnconfigure(1, weight=1)
        self.rootWindow.grid_rowconfigure(1, weight=1)
        self.rootWindow.title("Kassakreng")

        self.screen_width = self.rootWindow.winfo_screenwidth()
        self.screen_height = self.rootWindow.winfo_screenheight()

        self.setup_window_ui(self.rootWindow)
        #self.notecollection = KassaVuller(self.rootWindow, self.notecollection).get_value()
        self.rootWindow.mainloop()

    def setup_window_ui(self, window):
        self.eenheden_frame = tk.Frame(window, bg='red')
        self.eenheden_frame.pack(fill=tk.BOTH, expand=1, side=tk.TOP)
        bedrag_label = tk.Label(self.eenheden_frame, text="Bedrag", width=20,
                               font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD),
                               anchor="center")
        bedrag_label.grid(row=0, column=0, sticky="nsew")
        aantal_label = tk.Label(self.eenheden_frame, text="Aantal", width=20,
                                font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD),
                                anchor="center")
        aantal_label.grid(row=1, column=0, sticky="news")

        # voeg verschillende bedragen toe
        rekening = self.nieuw_rekening()
        self.eenheid_counter = 1
        for eenheid in rekening:
            self.__add_eenheden(self.eenheden_frame, eenheid)
        self.eenheden_frame.grid_columnconfigure(0, weight=1)
        self.eenheden_frame.grid_rowconfigure(0, weight=1)
        self.eenheden_frame.grid_rowconfigure(1, weight=1)

        self.fill_lower_frame(window)

    def fill_lower_frame(self, window):
        self.lower_frame = tk.Frame(window, bg='blue')
        self.lower_frame.pack(fill=tk.BOTH, expand=1, side=tk.BOTTOM)
        self.lower_frame.grid_rowconfigure(0, weight=1)

        clear_button = tk.Button(self.lower_frame, text="CLEAR",
                                   font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD),
                                   command=self.__button_clear)
        clear_button.grid(row=0, column=0, sticky="nsew")
        self.lower_frame.grid_columnconfigure(0, weight=1)

        ok_button = tk.Button(self.lower_frame, text="OK",
                                   font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD),
                                   command=self.__button_ok)
        ok_button.grid(row=0, column=1, sticky="nsew")
        self.lower_frame.grid_columnconfigure(1, weight=1)

        kassa_button = tk.Button(self.lower_frame, text="Kassa",
                                   font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD),
                                   command=self.__button_ok)
        kassa_button.grid(row=0, column=2, sticky="nsew")
        self.lower_frame.grid_columnconfigure(2, weight=1)

        send_button = tk.Button(self.lower_frame, text="Send",
                                   font=tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD),
                                   command=self.__button_ok)
        send_button.grid(row=0, column=3, sticky="nsew")
        self.lower_frame.grid_columnconfigure(3, weight=1)

    def __button_ok(self):
        rekening = 0
        keys = self.huidige_rekening.keys()
        keys.sort()
        for key in keys:
            rekening += self.huidige_rekening[key].bestelling.amount * key
            self.huidige_rekening[key].reset()

        print rekening

    def __button_clear(self):
        for key in self.huidige_rekening.keys():
            self.huidige_rekening[key].reset()

    def __add_eenheden(self, window, eenheid):
        nieuwe_eenheid = self.eenheidBestelling(eenheid)
        self.huidige_rekening[eenheid.bedrag] = nieuwe_eenheid
        eenheid_button = tk.Button(window, text=nieuwe_eenheid.bestelling.bedrag,
                                   font=tkFont.Font(family='Helvetica', size=50, weight=tkFont.BOLD),
                                   command=lambda: nieuwe_eenheid.plus_one())
        eenheid_button.grid(row=0, column=self.eenheid_counter, sticky="nsew")
        eenheid_label = tk.Label(window, textvariable=nieuwe_eenheid.tk_amount,
                                 font=tkFont.Font(family='Helvetica', size=50, weight=tkFont.BOLD))
        eenheid_label.grid(row=1, column=self.eenheid_counter, sticky="nsew")
        self.eenheden_frame.grid_columnconfigure(self.eenheid_counter, weight=1)
        self.eenheid_counter += 1

    def nieuw_rekening(self):
        return [Bestelling(1, 0),
                Bestelling(1.6, 0),
                Bestelling(2.2, 0),
                Bestelling(3.0, 0),
                Bestelling(12, 0)]



if __name__ == "__main__":
    kas = KassaSysteem()
