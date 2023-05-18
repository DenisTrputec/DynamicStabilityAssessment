from typing import List

import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from matplotlib import pyplot as plt


def read_csv(filepath: str) -> DataFrame:
    return pandas.read_csv(filepath, delimiter=', ', skiprows=1, encoding='latin-1', engine='python')


def filter_data(data: DataFrame, channels: list, filter_options: dict):
    """
    filter_options: {
        "type": str     # 'voltage_level', 'zone_number'
        "groups": list  # [400, 220, 110], [1, 2, 3, 4]
    }
    :return:
    """
    indexes = {x: []for x in filter_options["groups"]}

    for i, element in enumerate(channels):
        for key in indexes.keys():
            if filter_options["type"] == "voltage_level":
                if element.is_voltage_level(key):
                    indexes[key].append(i)
                    break
            elif filter_options["type"] == "zone_number":
                if element.is_zone_number(key):
                    indexes[key].append(i)
                    break

    new_data = {k: data.iloc[:, indexes[k]] for k, v in indexes.items()}
    return new_data


def plot_figure(x: Series, x_label: str, y_values: List[Series], y_labels: List[str],
                figure_path: str, figure_title: str = "", figure_size: tuple = (11.5, 9.5)
                ):
    figure, axes = plt.subplots(nrows=len(y_values), figsize=figure_size, sharex='all')
    figure.suptitle(figure_title)

    for axis, y, label in zip(axes, y_values, y_labels):
        for i, column in enumerate(y.columns):
            line_style = "solid" if i < 10 else "dashed"
            axis.plot(x, y[column], label=column, linestyle=line_style)
        axis.legend(loc='upper left', prop={'size': 6}, bbox_to_anchor=(1.01, 1), framealpha=1)
        axis.set_ylabel(label)
        axis.grid(linestyle='dotted')

    x_max = int(round(x.iloc[-1]))
    plt.xlabel(x_label)
    plt.xlim(0, x_max)
    plt.xticks([x / 10 for x in range(0, x_max * 10 + 1, x_max)])
    plt.savefig(figure_path)


if __name__ == "__main__":
    # data = read_csv("E:\\Python3\\DynamicStabilityAssessment\\output\\S10\\task1.csv")
    my_data = read_csv("E:\\Python3\\DynamicStabilityAssessment\\output\\S10\\task.csv")
    from power_system.bus import Bus
    my_channels = [
        Bus(1, "1", 400, 1, 1, 1),
        Bus(2, "2", 220, 1, 1, 1),
        Bus(3, "3", 220, 1, 1, 1),
        Bus(4, "4", 400, 1, 1, 1),
        Bus(5, "5", 110, 1, 1, 1),
    ]
    my_options = {
        "type": "voltage_level",
        "groups": [400, 220, 110]
    }
    y_dataframes = filter_data(my_data.iloc[:, 1:], my_channels, my_options)
    print(list(y_dataframes.values()))
    plot_figure(my_data.iloc[:, 0], "x", list(y_dataframes.values()), ["400", "220", "110"],
                "E:\\Python3\\DynamicStabilityAssessment\\output\\test.png", "My Title")
