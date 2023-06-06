import os
from typing import List

from dsa import psse
from dsa import plot
from dsa.assessment import Assessment
from dsa.model import Model
from dsa.scenario import Scenario
from options import Option, OptionType, GroupByType
from utils.logger import logger
from utils.system_manager import SystemManager


class Run:
    def __init__(self, output_folder: str, assessment: Assessment, model: Model, scenarios: List[Scenario],
                 options: List[Option], filters: dict):
        self.output_folder = os.path.join(output_folder, model.name)
        self.out_filepath = os.path.join(self.output_folder, "task.outx")
        self.csv_filepath = os.path.join(self.output_folder, "task.csv")
        self.assessment = assessment
        self.model = model
        self.scenarios = scenarios
        self.options = options
        self.filters = filters

        self.channels = {OptionType.BusU: [], OptionType.BranchP: []}
        self.current_index = 0
        self.current_scenario = self.scenarios[self.current_index]

        SystemManager.create_folder(self.output_folder)

    def set_next_scenario(self):
        self.current_index += 1
        if self.current_index < len(self.scenarios) - 1:
            self.current_scenario = self.scenarios[self.current_index]
            return True
        else:
            return False

    def initialize(self):
        logger.info("")
        functions = [(psse.initialize, None),
                     (psse.read_model_file, self.model.raw_path),
                     (psse.read_dynamics_file, self.model.dyr_path),
                     (psse.convert_model, None),
                     (psse.set_dynamic_parameters, None),
                     ]
        for f, arg in functions:
            err_msg = f(arg) if arg else f()
            if err_msg:
                return err_msg

    def add_channels(self):
        logger.info("")
        psse.reset_plot_channels()
        busses = psse.read_bus_data(filters=self.filters)
        branches = psse.read_branch_data(filters=self.filters)

        def add(elements, function, option_key):
            for element in elements:
                err_msg = function(element)
                if err_msg:
                    return err_msg
                else:
                    self.channels[option_key].append(element)

        for option in self.options:
            if option.in_use and option.type == OptionType.BusU:
                msg = add(busses.values(), psse.add_bus_u_channel, OptionType.BusU)
                if msg:
                    return msg
            elif option.in_use and option.type == OptionType.BranchP:
                msg = add(branches.values(), psse.add_branch_p_channel, OptionType.BranchP)
                if msg:
                    return msg

    def run_task(self):
        logger.info("")
        err_msg = psse.initialize_output(self.out_filepath)
        if err_msg:
            return err_msg

        for action in self.current_scenario.actions:
            err_msg = action.activate()
            if err_msg:
                return err_msg

        psse.save_output(self.out_filepath, self.csv_filepath)

    def save_output(self):
        logger.info("")
        data = plot.read_csv(self.csv_filepath)
        data_x = data.iloc[:, 0]

        option = [o for o in self.options if o.type == OptionType.BusU][0]
        options_page = {
            "type": option.group_by_page_type,
            "groups": option.group_by_page_values
        }
        data_pages, elements_pages = plot.filter_data(data.iloc[:, 1:], self.channels[option.type], options_page)
        options_subplot = {
            "type": option.group_by_subplot_type,
            "groups": option.group_by_subplot_values
        }
        # Create output folder for scenario pngs
        folder_path = os.path.join(self.output_folder, self.current_scenario.name)
        SystemManager.create_folder(folder_path)

        for i, (key, data_page) in enumerate(data_pages.items()):
            if option.group_by_subplot_in_use[i]:
                # Filtered data grouped by subplots
                data_subplots, _ = plot.filter_data(data_page, elements_pages[key], options_subplot)
                y_values = list(data_subplots.values())
                y_labels = list(data_subplots.keys())
            else:
                y_values = [data_page]
                y_labels = [key]

            figure_title = f"{self.assessment.name}\n" \
                           f"{self.model.description}\n" \
                           f"{self.current_scenario.description}"

            plot.plot_figure(x=data_x, x_label="Time(s)",
                             y_values=y_values, y_labels=y_labels,
                             figure_path=os.path.join(folder_path, f"{key}.png"), figure_title=figure_title)


if __name__ == "__main__":
    my_assessment = Assessment.load_from_json(
        "E:\\Python3\\DynamicStabilityAssessment\\assessments\\Procjena Dinamicke Stabilnosti.json")
    my_model = my_assessment.models[0]
    my_scenarios_used = [my_assessment.models[0].scenarios[0]]
    my_options = [Option(option_type=OptionType.BusU,
                         in_use=True,
                         group_by_page_type=GroupByType.VoltageLevel,
                         group_by_page_values=[400, 220, 110],
                         group_by_subplot_type=GroupByType.ZoneNumber,
                         group_by_subplot_values=[1, 3, 5],
                         group_by_subplots_in_use=[False, True, True]),
                  Option(option_type=OptionType.BranchP,
                         in_use=False,
                         group_by_page_type=GroupByType.VoltageLevel,
                         group_by_page_values=[400, 220, 110],
                         group_by_subplot_type=GroupByType.ZoneNumber,
                         group_by_subplot_values=[1, 3, 5],
                         group_by_subplots_in_use=[False, True, True])
                  ]
    my_run = Run(output_folder="E:\\Python3\\DynamicStabilityAssessment\\output\\test",
                 assessment=my_assessment,
                 model=my_model,
                 scenarios=my_scenarios_used,
                 options=my_options,
                 filters={})

    psse.silence()
    my_run.initialize()
    my_run.add_channels()
    my_run.run_task()
    psse.unsilence()
    my_run.save_output()
