import Tkinter as tk
import tkFont
import sqlite3
import os
import csv
from time import gmtime, strftime

from numericwindow import *
from totalwindow import *
from avondbedrag import *
from notecount import *
from bestelling import *
from sendmessage import *
from eindrekening import *


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
        self.setup_database()
        self.custom_totaal = 0
        self.setup_user_interface()

    def setup_database(self):
        try:
            self.db = sqlite3.connect("database.db")

            self.cursor = self.db.cursor()
            self.cursor.execute(
                "create table drinks(snack smallint, beer smallint, "
                "vedett smallint, wine smallint, bottle smallint, custom smallint, total smallint);"
            )
        except:
            pass

    def setup_user_interface(self):
        self.rootWindow = tk.Tk()
        myfont =tkFont.Font(family='Helvetica', size=28, weight=tkFont.BOLD)
        self.rootWindow.option_add('*Font', myfont)
        self.rootWindow.option_add('*Button*highlightThickness', 10)
        self.rootWindow.option_add('*Button*highlightBackground', 'white')
        self.rootWindow.option_add('*background', 'black')
        self.rootWindow.option_add('*foreground', 'white')
        self.rootWindow.attributes("-fullscreen", True)
        self.rootWindow.grid_columnconfigure(0, weight=1)
        self.rootWindow.grid_rowconfigure(0, weight=1)
        self.rootWindow.grid_columnconfigure(1, weight=1)
        self.rootWindow.grid_rowconfigure(1, weight=1)
        self.rootWindow.title("Kassakreng")
        self.eindrekening = EindRekening()

        self.screen_width = self.rootWindow.winfo_screenwidth()
        self.screen_height = self.rootWindow.winfo_screenheight()

        self.setup_window_ui(self.rootWindow)
        self.rootWindow.mainloop()

    def setup_window_ui(self, window):
        self.eenheden_frame = tk.Frame(window)
        self.eenheden_frame.pack(fill=tk.BOTH, expand=1, side=tk.TOP)
        bedrag_label = tk.Label(self.eenheden_frame, text="Bedrag", width=7, anchor="center")
        bedrag_label.grid(row=0, column=0, sticky="nsew")
        aantal_label = tk.Label(self.eenheden_frame, text="Aantal", width=7, anchor="center")
        aantal_label.grid(row=1, column=0, sticky="news")

        # voeg verschillende bedragen toe
        rekening = self.nieuw_rekening()
        self.eenheid_counter = 1
        for eenheid in rekening:
            self.__add_eenheden(self.eenheden_frame, eenheid)
        self.__add_mystery_knop(self.eenheden_frame)
        self.eenheden_frame.grid_columnconfigure(0, weight=1)
        self.eenheden_frame.grid_rowconfigure(0, weight=1)
        self.eenheden_frame.grid_rowconfigure(1, weight=1)

        self.fill_lower_frame(window)

    def fill_lower_frame(self, window):
        self.lower_frame = tk.Frame(window)
        self.lower_frame.pack(fill=tk.BOTH, expand=1, side=tk.BOTTOM)
        self.lower_frame.grid_rowconfigure(0, weight=1)
        self.lower_frame.grid_rowconfigure(1, weight=1)

        clear_button = tk.Button(self.lower_frame, text="Reset",
                                 command=self.__button_clear)
        clear_button.grid(row=0, column=0, sticky="nsew", rowspan=2)
        self.lower_frame.grid_columnconfigure(0, weight=1)

        ok_button = tk.Button(self.lower_frame, text="OK", command=self.__button_ok)
        ok_button.grid(row=0, column=1, sticky="nsew", rowspan=2)
        self.lower_frame.grid_columnconfigure(1, weight=1)

        send_button = tk.Button(self.lower_frame, text="Avondtotaal", command=self.__button_total)
        send_button.grid(row=0, column=2, sticky="nsew")
        total_button = tk.Button(self.lower_frame, text="Send", command=self.__button_send)
        total_button.grid(row=1, column=2, sticky="nsew")
        self.lower_frame.grid_columnconfigure(2, weight=1)

    def leeg_database(self):
        self.cursor.execute('DELETE FROM drinks')
        self.db.commit()

    def maak_excel(self):
        self.cursor.execute('SELECT * FROM drinks')
        timestring = strftime("%Y-%m-%d-%Hh%Mm%Ss", gmtime())
        with open("/home/pi/csvs/" + timestring + ".csv", "wb") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in self.cursor.description])
            csv_writer.writerows(self.cursor)

    def __button_total(self):
        self.cursor.execute('SELECT sum(total) FROM drinks')
        totaal =  self.cursor.fetchone()[0]
        if AvondBedrag(self.rootWindow, totaal).einde:
            self.maak_excel()
            self.leeg_database()
            self.__button_clear()
        else:
            pass

    def __button_ok(self):
        rekening = 0
        bestelling = []
        keys = self.huidige_rekening.keys()
        keys.sort()
        insertstring = "INSERT INTO drinks VALUES("
        for key in keys:
            eenheidrekening = self.huidige_rekening[key]
            insertstring += str(eenheidrekening.bestelling.amount) + ","
            bestelling.append(eenheidrekening.bestelling)
            rekening += eenheidrekening.bestelling.amount * key
        rekening += self.custom_totaal
        insertstring = insertstring[:-1] + "," + str(self.custom_totaal) +"," + str(rekening) + ");"

        if TotalWindow(self.rootWindow, rekening).has_agreed():
            self.__button_clear()
            self.eindrekening.add_rekening(bestelling)
            self.cursor.execute(insertstring)
            self.db.commit()

    def __button_clear(self):
        for key in self.huidige_rekening.keys():
            self.huidige_rekening[key].reset()
        self.custom_totaal = 0
        self.totaalvar.set(0)

    def __button_mystery(self):
        self.custom_totaal += NumericWindow(self.rootWindow).get_value()
        self.totaalvar.set(self.custom_totaal)

    def __button_send(self):
        directorycontent = os.listdir("/media/pi/")
        if len(directorycontent) == 0:
            MessageWindow(self.rootWindow, "Geen USB stick gevonden")
        else:
            os.system("cp /home/pi/csvs/* /media/pi/" + directorycontent[0])
            os.system("sync")
            MessageWindow(self.rootWindow, "Alle CSV's gekopieerd naar USB stick")

    def __add_mystery_knop(self, window):
        self.totaalvar = tk.IntVar()
        mystery_button = tk.Button(window, text="Custom", command=self.__button_mystery)
        mystery_button.grid(row=0, column=self.eenheid_counter, sticky="nsew")
        self.eenheden_frame.grid_columnconfigure(self.eenheid_counter, weight=1)
        mystery_var = tk.Label(window, textvariable=self.totaalvar)
        mystery_var.grid(row=1, column=self.eenheid_counter, sticky="nsew")


    def __add_eenheden(self, window, eenheid):
        nieuwe_eenheid = self.eenheidBestelling(eenheid)
        self.huidige_rekening[eenheid.bedrag] = nieuwe_eenheid
        eenheid_button = tk.Button(window, text=nieuwe_eenheid.bestelling.bedrag,
                                   command=lambda: nieuwe_eenheid.plus_one())
        eenheid_button.grid(row=0, column=self.eenheid_counter, sticky="nsew")
        eenheid_label = tk.Label(window, textvariable=nieuwe_eenheid.tk_amount)
        eenheid_label.grid(row=1, column=self.eenheid_counter, sticky="nsew")
        self.eenheden_frame.grid_columnconfigure(self.eenheid_counter, weight=1)
        self.eenheid_counter += 1

    def nieuw_rekening(self):
        return [Bestelling(1, 0),
                Bestelling(1.6, 0),
                Bestelling(2.2, 0),
                Bestelling(3.3, 0),
                Bestelling(15, 0)]


if __name__ == "__main__":
    kas = KassaSysteem()
