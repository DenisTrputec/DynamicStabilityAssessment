import os
from typing import TYPE_CHECKING, List

from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from dsa import psse
from dsa.model import Model
from dsa.scenario import Scenario
from utils.logger import logger
from utils.system_manager import SystemManager

if TYPE_CHECKING:
    from ui_py.ui_run_options import UIRunOptions


class UIRun(QMainWindow):
    def __init__(self, parent: "UIRunOptions", output_folder: str, model: Model, scenarios: List[Scenario],
                 options: dict, filters: dict):
        logger.info("")
        super().__init__()
        uic.loadUi("ui/run.ui", self)
        self.__child = None
        self.__output_folder = os.path.join(output_folder, model.name)
        self.__model = model
        self.__scenarios = scenarios
        self.__options = options
        self.__filters = filters

        self.parent = parent
        self.parent.hide()
        self.set_window()

        SystemManager.create_folder(self.__output_folder)

        self.pb_run.clicked.connect(self.run_process)

    def set_window(self):
        logger.info("")
        self.lbl_model.setText(self.__model.name)
        self.show()

    def set_text_to_default(self):
        logger.info("")
        self.lbl_initialize.setText("")
        self.lbl_task1.setText("")

    def run_process(self):
        logger.info("")
        for index, scenario in enumerate(self.__scenarios):
            self.set_text_to_default()
            if not self.initialize(index, scenario):
                break
            if not self.add_channels():
                break
            return
            if not self.run_task(scenario):
                break

    def initialize(self, index: int, scenario: Scenario):
        logger.info("")
        self.lbl_initialize.setText("Running")
        self.lbl_scenario.setText(f"{scenario.name}   {index + 1}/{len(self.__scenarios)}")
        functions = [(psse.initialize, None),
                     (psse.read_model_file, self.__model.raw_path),
                     (psse.read_dynamics_file, self.__model.dyr_path),
                     (psse.convert_model, None),
                     (psse.set_dynamic_parameters, None),
                     ]
        for f, arg in functions:
            err_msg = f(arg) if arg else f()
            if err_msg:
                self.lbl_initialize.setText(err_msg)
                return False
        self.lbl_initialize.setText("Done")
        return True

    def add_channels(self):
        psse.reset_plot_channels()
        busses = psse.read_bus_data(filters=self.__filters)
        branches = psse.read_branch_data()
        for bus in busses.values():
            if self.__options["bus_u"]:
                err_msg = psse.add_voltage_channel(bus)
                if err_msg:
                    self.lbl_task1.setText(f"Error: {err_msg}")
                    return False
        return True

    def run_task(self, scenario: Scenario):
        logger.info("")
        self.lbl_task1.setText("Running")

        err_msg = psse.initialize_output(os.path.join(self.__output_folder, "task1.outx"))
        if err_msg:
            self.lbl_task1.setText(err_msg)
            return False

        for action in scenario.actions:
            action.activate()

        psse.save_output(os.path.join(self.__output_folder, "task1.outx"), os.path.join(self.__output_folder, "task1.csv"))

        self.lbl_task1.setText("Done")
        return True

    def closeEvent(self, event):
        logger.info("")
        self.parent.show()
        event.accept()
