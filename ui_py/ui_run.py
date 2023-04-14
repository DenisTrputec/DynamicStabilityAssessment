from typing import TYPE_CHECKING, List

from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from dsa.model import Model
from dsa.scenario import Scenario
from dsa.psse import PSSE
from utils.logger import logger

if TYPE_CHECKING:
    from ui_py.ui_run_options import UIRunOptions


class UIRun(QMainWindow):
    def __init__(self, parent: "UIRunOptions", output_folder: str, model: Model, scenarios: List[Scenario]):
        logger.info("")
        super().__init__()
        uic.loadUi("ui/run.ui", self)
        self.__child = None
        self.__output_folder = output_folder
        self.__model = model
        self.__scenarios = scenarios

        self.parent = parent
        self.parent.hide()
        self.set_window()
        self.run_process()

    def set_window(self):
        logger.info("")
        self.lbl_model.setText(self.__model.name)
        self.show()

    def run_process(self):
        for i, scenario in enumerate(self.__scenarios):
            self.lbl_initialize.setText("Running")
            self.lbl_scenario.setText(f"{scenario.name} {i+1}/{len(self.__scenarios)}")
            PSSE.initialize()
            PSSE.read_raw(self.__model.raw_path)
            PSSE.read_dyr(self.__model.dyr_path)
            PSSE.set_dynamic_parameters()
            self.lbl_initialize.setText("Done")

    def closeEvent(self, event):
        logger.info(f"")
        self.parent.show()
        event.accept()
