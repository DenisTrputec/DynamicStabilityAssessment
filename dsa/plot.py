from typing import List

import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from matplotlib import pyplot as plt


def read_csv(filepath: str) -> DataFrame:
    return pandas.read_csv(filepath, delimiter=', ', skiprows=1, encoding='latin-1', engine='python')


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
    data = read_csv("E:\\Python3\\DynamicStabilityAssessment\\output\\temp.csv")

    y1 = data.iloc[:, 1:15]
    y2 = data.iloc[:, 15:19]

    plot_figure(data.iloc[:, 0], "x", [y1, y2], ["y1", "y2"],
                "E:\\Python3\\DynamicStabilityAssessment\\output\\test.png", "My Title")
