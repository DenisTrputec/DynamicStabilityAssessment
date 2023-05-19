import os
from typing import List

from dsa import psse
from dsa import plot
from dsa.model import Model
from dsa.scenario import Scenario
from options import Option, OptionType, GroupByType
from utils.logger import logger
from utils.system_manager import SystemManager


class Run:
    def __init__(self, output_folder: str, model: Model, scenarios: List[Scenario], options: List[Option],
                 filters: dict):
        self.output_folder = os.path.join(output_folder, model.name)
        self.out_filepath = os.path.join(self.output_folder, "task.outx")
        self.csv_filepath = os.path.join(self.output_folder, "task.csv")
        self.model = model
        self.scenarios = scenarios
        self.options = options
        self.filters = filters

        self.channels = []
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

        def add(elements, function):
            for element in elements:
                err_msg = function(element)
                if err_msg:
                    return err_msg
                else:
                    self.channels.append(element)

        for option in self.options:
            if option.in_use and option.type == OptionType.BusU:
                msg = add(busses.values(), psse.add_bus_u_channel)
                if msg:
                    return msg
            elif option.in_use and option.type == OptionType.BranchP:
                msg = add(branches.values(), psse.add_branch_p_channel)
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
        print(data)


if __name__ == "__main__":
    from dsa.assessment import Assessment

    my_assessment = Assessment.load_from_json(
        "E:\\Python3\\DynamicStabilityAssessment\\assessments\\Procjena Dinamicke Stabilnosti.json")
    my_model = my_assessment.models[0]
    my_scenarios_used = [my_assessment.models[0].scenarios[0]]
    my_options = [Option(option_type=OptionType.BusU,
                         in_use=True,
                         group_by_page_type=GroupByType.VoltageLevel,
                         group_by_page_values=[400, 220, 110],
                         group_by_subplot_type=GroupByType.ZoneNumber,
                         group_by_subplot_values=[1, 2, 3, 4],
                         group_by_subplots_in_use=[False, True, True]),
                  Option(option_type=OptionType.BranchP,
                         in_use=False,
                         group_by_page_type=GroupByType.VoltageLevel,
                         group_by_page_values=[400, 220, 110],
                         group_by_subplot_type=GroupByType.ZoneNumber,
                         group_by_subplot_values=[1, 2, 3, 4],
                         group_by_subplots_in_use=[False, True, True])
                  ]
    my_run = Run(output_folder="E:\\Python3\\DynamicStabilityAssessment\\output\\test",
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
