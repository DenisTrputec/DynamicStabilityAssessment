import os
from typing import TYPE_CHECKING, List

from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from dsa.model import Model
from dsa.scenario import Scenario
from dsa.psse import PSSE
from utils.logger import logger
from utils.system_manager import SystemManager

if TYPE_CHECKING:
    from ui_py.ui_run_options import UIRunOptions


class UIRun(QMainWindow):
    def __init__(self, parent: "UIRunOptions", output_folder: str, model: Model, scenarios: List[Scenario],
                 options: dict):
        logger.info("")
        super().__init__()
        uic.loadUi("ui/run.ui", self)
        self.__child = None
        self.__output_folder = os.path.join(output_folder, model.name)
        self.__model = model
        self.__scenarios = scenarios

        self.parent = parent
        self.parent.hide()
        self.set_window()

        SystemManager.create_folder(self.__output_folder)
        self.run_process()

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
            self.initialize(index, scenario)
            if not self.run_task(scenario):
                break

    def initialize(self, index: int, scenario: Scenario):
        logger.info("")
        self.lbl_initialize.setText("Running")
        self.lbl_scenario.setText(f"{scenario.name}   {index + 1}/{len(self.__scenarios)}")
        PSSE.initialize()
        PSSE.read_raw(self.__model.raw_path)
        PSSE.read_dyr(self.__model.dyr_path)
        PSSE.set_dynamic_parameters()
        self.lbl_initialize.setText("Done")

    def run_task(self, scenario: Scenario):
        logger.info("")
        self.lbl_task1.setText("Running")

        PSSE.reset_plot_channels()
        busses = PSSE.read_bus_data()
        for bus in busses.values():
            err_msg = PSSE.add_voltage_channel(bus)
            if err_msg:
                self.lbl_task1.setText(f"Error: {err_msg}")
                return False
            break

        err_msg = PSSE.initialize_output(os.path.join(self.__output_folder, "task1.outx"))
        if err_msg:
            self.lbl_task1.setText(err_msg)
            return False
        self.lbl_task1.setText("Done")
        return True

    def closeEvent(self, event):
        logger.info("")
        self.parent.show()
        event.accept()
