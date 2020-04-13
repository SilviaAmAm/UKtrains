import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter, HourLocator
import seaborn as sns
sns.set()


def convert_to_datetimes(data):
    """
    :param data: array of times in format hour:min
    :return:
    """
    return datetime.datetime.strptime(row[1], "%H:%M")

data = np.load('gwr_thameslink.npz')

for array_name in ['arr_0', 'arr_1']:
    train_company_data = data[array_name]

    sched_dep = []
    actual_dep = []
    sched_arr = []
    actual_arr = []

    for row in train_company_data:
        sched_dep.append(convert_to_datetimes(row[1]))
        actual_dep.append(convert_to_datetimes(row[2]))
        sched_arr.append(convert_to_datetimes(row[3]))
        actual_arr.append(convert_to_datetimes(row[4]))

    fig, ax = plt.subplots(ncols=2, figsize=(10, 6))

    ax[0].plot_date(date2num(sched_dep), date2num(actual_dep), label="Departures", color=sns.color_palette()[0])
    ax[0].set_xlabel("Scheduled departure time")
    ax[0].set_ylabel("Actual departure time")

    min_val = date2num(datetime.datetime.strptime("07:00", "%H:%M"))
    max_val = date2num(datetime.datetime.strptime("22:00", "%H:%M"))
    lims = (min_val, max_val)
    ax[0].set_ylim(lims)
    ax[0].set_xlim(lims)
    myFmt = DateFormatter('%H:00')
    locator = HourLocator(interval=3)
    ax[0].xaxis.set_major_formatter(myFmt)
    ax[0].xaxis.set_major_locator(locator)
    ax[0].yaxis.set_major_formatter(myFmt)
    ax[0].yaxis.set_major_locator(locator)
    ax[0].set_aspect(aspect='equal')
    ax[0].legend()

    ax[1].plot_date(date2num(sched_arr), date2num(actual_arr), label="Arrivals", color=sns.color_palette()[1])
    ax[1].xaxis.set_major_formatter(myFmt)
    ax[1].yaxis.set_major_formatter(myFmt)
    ax[1].set_xlabel("Scheduled arrival time")
    ax[1].set_ylabel("Actual arrival time")
    ax[1].set_aspect(aspect='equal')
    ax[1].set_xlim(lims)
    ax[1].xaxis.set_major_locator(locator)
    ax[1].set_ylim(lims)
    ax[1].yaxis.set_major_locator(locator)
    ax[1].legend()

    plt.tight_layout()

    if array_name == 'arr_0':
        name = "GWR"
    else:
        name = "Thameslink"

    plt.savefig(f"./plots/{name}_correlation.png", dpi=150)
