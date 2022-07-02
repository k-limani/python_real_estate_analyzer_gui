"""
    Provides a main window that lets the user choose to view the price
    trend or to compare prices, a dialog window that lets the user choose one 
    or more cities for the rental trend plot, and a plot window that shows 
    either one of the two plots.
"""
import matplotlib  # pip install matplotlib
import tkinter as tk  # pip install tk
import matplotlib.pyplot as plt
from rent import Rent
import tkinter.messagebox as tkmb

# pip install PyQt5
matplotlib.use("Qt5Agg")  # tell matplotlib to work with Tkinter (before "TkAgg")

# pip install --upgrade --force-reinstall Pillow
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # canvas widget

CITIES = [
    "San Jose",
    "Santa Clara",
    "Milpitas",
    "Los Gatos",
    "Cupertino",
    "Campbell",
    "Palo Alto",
    "Sunnyvale",
    "Mountain View",
]
STANDARD_FONT = ("Arial", 11)


class MainWin(tk.Tk):
    """Graphs avg and current rental price trends in the Bay Area"""

    def __init__(self):
        super().__init__()

        # attributes
        self.geometry("420x140+450+200")
        self.title("Bay Area Rent Statistics")
        self.btn_click = tk.StringVar()

        try:
            self.rent = Rent()
        except OSError as e:
            err_msg = tkmb.showerror("Error:", str(e), parent=self)
            if err_msg == "ok":
                self.destroy()

        # frame
        frame = tk.Frame(self, pady=10, borderwidth=1)
        frame.pack(anchor=tk.CENTER, expand=True)

        # label and buttons
        BTN_TXTS = "Average Price Trends", "Current Price Trends"

        # create the components and pack them together
        tk.Label(
            frame,
            text="Rental Stats Calculator for Bay Area",
            fg="purple",
            font=("Arial", 16, "italic"),
        ).pack(side=tk.TOP, padx=10, pady=10)

        [
            tk.Button(
                frame,
                text=elem,
                font=STANDARD_FONT,
                command=lambda x=elem, f=self.display: f(x),
            ).pack(side=tk.LEFT, padx=10)
            for elem in BTN_TXTS
        ]

    def display(self, x):
        """shows current trends graphic or redirets user
        to ratio buttons list"""

        self.btn_click.set(x)
        if "Current" in x:
            plotwin = PlotWin(self, self.rent)
            plotwin.show_plot(self.btn_click)
        elif "Average" in x:
            DialogWin(self, self.rent)


class DialogWin(tk.Toplevel):
    """user can chose one city or all areas to show the rental rent graph """

    def __init__(self, master, dataprocessor):
        super().__init__(master)

        # width, height, location on screen of top left corner
        self.geometry("200x400")

        self.title("City Selection")

        # Moves the keyboard focus to this widget
        self.focus_set()

        # Routes all events for this application to this widget
        self.grab_set()

        # always drawn on top of its master, and is automatically
        # hidden when the master is iconified
        self.transient(master)

        self.master = master
        self.rent = dataprocessor

        # frame
        frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1, padx=10, pady=10)

        frame.pack(fill=tk.BOTH, expand=True)

        # selected radio button
        rad_selection = tk.StringVar()
        rad_selection.set("San Jose")  # initializing the choice to pre-select

        rad_btns = [
            tk.Radiobutton(
                frame,
                text=city,
                font=STANDARD_FONT,
                variable=rad_selection,
                value=city,
                command=lambda: rad_selection.get(),
            ).pack(anchor=tk.W, padx=5, pady=5)
            for city in CITIES
        ]

        rad_btns.append(
            tk.Radiobutton(
                frame,
                text="All",
                font=STANDARD_FONT,
                variable=rad_selection,
                value="All",
                command=lambda: rad_selection.get(),
            ).pack(anchor=tk.W, padx=5, pady=5)
        )

        tk.Button(
            self,
            text="OK",
            font=STANDARD_FONT,
            padx=20,
            command=lambda x=rad_selection, f=self.display: f(x),
        ).pack(anchor=tk.W, padx=5, pady=5)

    def display(self, x):
        """calles appropriate DataProcessor plotting func depending
        on/if city selection"""

        plotwin = PlotWin(self.master, self.rent)  # as a child window
        plotwin.show_plot(x)


class PlotWin(tk.Toplevel):  # as child windows
    """docstrings"""

    def __init__(self, master, dataprocessor):
        super().__init__(master)
        self.rent = dataprocessor

    def show_plot(self, s):
        # width, height, location on screen of top left corner
        self.geometry("600x600")
        fig = plt.figure(figsize=(6, 6))
        var = s.get()
        if "Current" in var:
            self.rent.plot_recent_data()
            self.title("Current Price Trends")
        elif "All" in var:
            self.rent.plot_avg_data(isAllCities=True)
            self.title("Average Price Trends for All Areas")
        else:
            self.rent.plot_avg_data(city=var, isAllCities=False)
            self.title("Average Price Trends for " + var)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack()
        canvas.draw()


app1 = MainWin()
app1.mainloop()
