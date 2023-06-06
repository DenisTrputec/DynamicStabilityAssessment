import os
from typing import List, Tuple

import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from matplotlib import pyplot as plt

from options import OptionType, GroupByType


def read_csv(filepath: str) -> DataFrame:
    return pandas.read_csv(filepath, delimiter=', ', skiprows=1, encoding='latin-1', engine='python')


def filter_data(data: DataFrame, channels: list, filter_options: dict) -> Tuple[dict, dict]:
    """
    filter_options: {
        "type": GroupByType # GroupByType.VoltageLevel, GroupByType.ZoneNumber
        "groups": list      # [400, 220, 110], [1, 2, 3, 4]
    }
    :return:
    """
    indexes = {x: []for x in filter_options["groups"]}
    filtered_elements = {x: []for x in filter_options["groups"]}
    for i, element in enumerate(channels):
        for key in indexes.keys():
            if filter_options["type"] == GroupByType.VoltageLevel:
                if element.is_voltage_level(key):
                    indexes[key].append(i)
                    filtered_elements[key].append(element)
                    break
            elif filter_options["type"] == GroupByType.ZoneNumber:
                if element.is_zone_number(key):
                    indexes[key].append(i)
                    filtered_elements[key].append(element)
                    break

    new_data = {k: data.iloc[:, indexes[k]] for k, v in indexes.items()}
    return new_data, filtered_elements


def plot_figure(x: Series, x_label: str, y_values: List[Series], y_labels: List[str],
                figure_path: str, figure_title: str = "", figure_size: tuple = (11.5, 9.5)
                ):
    if len(y_values) < 3:
        figure_size = (11.5, 5.5)
    figure, axes = plt.subplots(nrows=len(y_values), figsize=figure_size, sharex='all')
    figure.suptitle(figure_title)
    if len(y_values) == 1:
        axes = [axes]
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
    my_data = read_csv("E:\\Python3\\DynamicStabilityAssessment\\output\\S10\\task.csv")

    from power_system.bus import Bus
    my_channels = {
        OptionType.BusU: [
            Bus(1, "1", 400, 1, 1, 1),
            Bus(2, "2", 220, 1, 1, 1),
            Bus(3, "3", 220, 1, 1, 2),
            Bus(4, "4", 400, 1, 1, 1),
            Bus(5, "5", 110, 1, 1, 3),
        ]
    }

    my_options = {
        "type": GroupByType.VoltageLevel,
        "groups": [400, 220, 110]
    }
    y_dataframes, _ = filter_data(my_data.iloc[:, 1:], my_channels[OptionType.BusU], my_options)
    plot_figure(my_data.iloc[:, 0], "x", list(y_dataframes.values()), ["400", "220", "110"],
                "E:\\Python3\\DynamicStabilityAssessment\\output\\test.png", "My Title")

    my_options2 = {
        "type": GroupByType.ZoneNumber,
        "groups": [1, 2, 3, 4]
    }
    y_dataframes2, _ = filter_data(my_data.iloc[:, 1:], my_channels[OptionType.BusU], my_options2)
    plot_figure(my_data.iloc[:, 0], "x", list(y_dataframes2.values()), ["Zona 1", "Zona 2", "Zona 3", "Zona 4"],
                "E:\\Python3\\DynamicStabilityAssessment\\output\\test2.png", "My Title")
