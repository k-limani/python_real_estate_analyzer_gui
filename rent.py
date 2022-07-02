"""
    rent.py reads data from cities.csv and backup.csv, calculate the mean
    rental prices for a city across all of its zip codes, plots the price 
    trend for one or more cities, and plots the most current rental price 
    for each zip code.
"""

from datetime import datetime
from dateutil.rrule import rrule, MONTHLY
import matplotlib.pyplot as plt
import numpy as np

CSVFILES = "cities.csv", "rent.csv"


# decorator
def printNums(method):  # printNums(self) #if it was part of the class
    """Decorator function prints to the output screen the return value
    of the function."""

    def wrapper(*args, **kwargs):
        # self(*args, **kwargs) #if it was part of the class
        result = method(*args, **kwargs)
        print()
        print(result)
        return result

    return wrapper


class Rent:

    def __init__(self):
        """ Constructor for Rent class """
        # data from may 2018 to august 2019, total 16 months
        self.start_month = 5
        self.start_year = 2018
        self.end_month = 8
        self.end_year = 2019
        self.read_data(CSVFILES)

        self.avgs = self.calc_mean_matrix()

    def read_data(self, *args):
        # reads the zip codes and city names into arr structures,
        # reads the rental prices into a numpy array
        fct = lambda x, y: np.loadtxt(x, dtype=y, delimiter=",")
        for cities, rents in args:
            self.cities, self.rents = fct(cities, str), fct(rents, float)
            try:
                self.cities, self.rents = fct(cities, str), fct(rents, float)
            except ValueError:
                self.cities, self.rents = fct(rents, str), fct(cities, float)
            except IOError as e:
                raise IOError("\n----> Exception file not found:", str(e))
                raise SystemExit
            except AttributeError:
                raise AttributeError("\n----> attribute error")
                raise SystemExit

    @printNums
    def calc_mean_matrix(self):
        """Calculates the mean monthly rental price for one city across
         time for its zip code"""

        return np.round(
            [
                np.mean(self.rents[np.argwhere(x == self.cities)[:, 0]], axis=0)
                for x in np.unique(self.cities[:, 1])
            ],
            1,
        )
        # list(dict.fromkeys(self.cities[:,1]))], 1)

    def plot_avg_data(self, city="", isAllCities=False):
        """ Plots the rental price trend for one c or isAllCities c """
        avgs = self.avgs
        sorted_cities = np.unique(self.cities[:, 1])

        m_yr = [
            str(x.month) + "/" + str(x.year)
            for x in rrule(
                MONTHLY,
                dtstart=datetime(self.start_year, self.start_month, 1),
                until=datetime(self.end_year, self.end_month, 1),
            )
        ]

        fct = lambda x: plt.plot(
            avgs[np.argwhere(sorted_cities == x)[0, 0]], label=x
        )  # choose city to plot

        if isAllCities == True:
            for c in sorted_cities:
                fct(c)
            plt.legend(loc="upper left", fontsize=8)
            plt.ylim(np.min(avgs) - 100, np.max(avgs) + 200)
        elif city in sorted_cities:
            fct(city)
            plt.legend(loc="best")
        else:
            raise AttributeError

        plt.title("Rental prices over time")  # title
        plt.ylabel("Rental prices (dollars)")  # y-axis label
        plt.xticks(range(0, len(m_yr)), m_yr, rotation=90)
        plt.xlim(-1, len(m_yr))
        plt.grid(color="grey", linestyle=":", linewidth=0.2)

        plt.tight_layout()

    #         plt.show()

    def _bar_auto_label(self, barplot: plt.bar, x_labels: list):
        # takes plt.bar object, a list of labels for x,
        # and positions labels at top of bars

        # get y-axis height to calculate label position from
        y_bottom, y_top = plt.gca().get_ylim()

        y_height = y_top - y_bottom
        for i, rect in enumerate(barplot):
            height = rect.get_height()
            x = rect.get_x() + rect.get_width() / 1.8
            y = height + (y_height * -0.022)  # variable height labels
            plt.text(
                x,  # takes your x values as horizontal positioning argument
                y,  # takes your y values as vertical positioning argument
                s=x_labels[i],  # the labels you want to add to the data
                va="center_baseline",  # vertical alignment
                ha="center",  # horizontal alignment
                rotation=90,
            )  # rotation

            # disables xticks below xaxis so they don't show twice
            plt.xticks([])

    @printNums
    def plot_recent_data(self):
        """ Plots the most current rental price for each zip code """
        current_rents = np.sort(np.array(self.rents[:, -1]))
        print("current_rents=", current_rents)
        cities = self.cities

        cit_zip = [
            str(elem[0] + " " + elem[1])
            for elem in np.concatenate((cities[0:0, [0, 1]], cities[:, [1, 0]]), axis=0)
        ]

        # b in case of _bar_auto_label usage
        b = plt.bar(cit_zip, current_rents, color="gold", width=0.75)

        plt.title("Latest prices by zip code")  # title
        plt.ylabel("Latest backup prices")  # x-axis label
        plt.ylim(1600, current_rents[-1] + 100)

        # shows xticks below x axis
        plt.xticks(np.arange(0, len(cit_zip)), cit_zip, rotation=90)

        # shows xticks (city names) over the bars instead, otherwise names appear below
        # self._bar_auto_label(b, cit_zip)

        # Automatically adjust subplot parameters to give specified padding
        plt.tight_layout()

        #         plt.show()

        return current_rents


def test_driver():
    """Main kai_bash_in_python driver which will do the unit
    testing of all the functions/methods above"""
    dataprocessor = Rent()
    dataprocessor.plot_avg_data("Campbell")
    dataprocessor.plot_avg_data(isAllCities=True)
    dataprocessor.plot_recent_data()


testdriver = test_driver()
