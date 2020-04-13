import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
sns.set()


def get_delta_times(data):
    """
    :param data: an array with four columns corresponding to Scheduled Departure, Actual Departure, 
    Scheduled Arrival and Actual Arrival times.
    :return: A dictionary with a 'Delta Departure' and 'Delta Arrival' keys
    """
    delta_times = {
        'Delta Departure': [],
        'Delta Arrival': [],
    }

    for row in data:
        sched_dep = datetime.datetime.strptime(row[1], "%H:%M")
        actual_dep = datetime.datetime.strptime(row[2], "%H:%M")
        if actual_dep >= sched_dep:
            delta_times['Delta Departure'].append((actual_dep - sched_dep).seconds)
        else:
            delta_times['Delta Departure'].append(-(sched_dep - actual_dep).seconds)

        sched_arr = datetime.datetime.strptime(row[3], "%H:%M")
        actual_arr = datetime.datetime.strptime(row[4], "%H:%M")
        if actual_arr >= sched_arr:
            delta_times['Delta Arrival'].append((actual_arr - sched_arr).seconds)
        else:
            delta_times['Delta Arrival'].append(-(sched_arr - actual_arr).seconds)
            
    return delta_times


def get_bins(delta_times):
    return np.arange(
        min(min(delta_times['Delta Departure']), min(delta_times['Delta Arrival'])),
        max(max(delta_times['Delta Departure']) + 1, max(delta_times['Delta Arrival']) + 1),
        60
    )
    

data = np.load('gwr_thameslink.npz')

for array_name in ['arr_0', 'arr_1']:
    train_company_data = data[array_name]
    delta_times = get_delta_times(train_company_data)

    bins = get_bins(delta_times)

    hist_departure, bin_departure = np.histogram(
        delta_times['Delta Departure'],
        bins=bins,
        density=False
    )

    hist_arrival, bin_arrival = np.histogram(
        delta_times['Delta Arrival'],
        bins=bins,
        density=False
    )

    fig, ax = plt.subplots(nrows=2, sharex='col')
    bins_labels = [int(bin_value/60.0) for bin_value in bins]

    ax[0].bar(bins_labels[:-1], hist_arrival, label="Arrivals", width=1, color=sns.color_palette()[0])
    ax[0].legend()
    ax[0].yaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))

    ax[1].bar(bins_labels[:-1], hist_departure, label="Departures", width=1, color=sns.color_palette()[1])
    ax[1].legend()
    ax[1].set_xlabel("Difference between scheduled and actual time (minutes)")

    fig.text(0.05, 0.5, 'Number of occurrences', ha='center', va='center', rotation='vertical')
    if array_name == 'arr_0':
        name = "GWR"
    else:
        name = "Thameslink"

    plt.savefig(f"./plots/{name}_histograms.png", dpi=150)
