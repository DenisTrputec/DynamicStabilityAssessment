import os
from typing import TYPE_CHECKING, List

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from dsa import psse
from dsa import plot
from dsa.model import Model
from dsa.scenario import Scenario
from utils.logger import logger
from utils.system_manager import SystemManager

if TYPE_CHECKING:
    from ui_py.ui_run_options import UIRunOptions


class Worker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, parent):
        super(QThread, self).__init__()
        self.parent = parent

    def initialize(self):
        logger.info("")
        functions = [(psse.initialize, None),
                     (psse.read_model_file, self.parent.model.raw_path),
                     (psse.read_dynamics_file, self.parent.model.dyr_path),
                     (psse.convert_model, None),
                     (psse.set_dynamic_parameters, None),
                     ]
        for f, arg in functions:
            err_msg = f(arg) if arg else f()
            if err_msg:
                self.finished.emit("Initialize: " + err_msg)
        self.finished.emit("Initialize: Done")

    def add_channels(self):
        logger.info("")
        psse.reset_plot_channels()
        busses = psse.read_bus_data(filters=self.parent.filters)
        branches = psse.read_branch_data(filters=self.parent.filters)
        for bus in busses.values():
            if self.parent.options["bus_u"]:
                err_msg = psse.add_bus_u_channel(bus)
                if err_msg:
                    self.finished.emit("Add Channels: " + err_msg)
        for branch in branches.values():
            if self.parent.options["branch_p"]:
                err_msg = psse.add_branch_p_channel(branch)
                if err_msg:
                    self.finished.emit("Add Channels: " + err_msg)
        self.finished.emit("Add Channels: Done")

    def run_task(self):
        logger.info("")
        err_msg = psse.initialize_output(self.parent.out_filepath)
        if err_msg:
            self.finished.emit("Task: " + err_msg)

        for action in self.parent.current_scenario.actions:
            action.activate()

        psse.save_output(self.parent.out_filepath, self.parent.csv_filepath)
        self.finished.emit("Task: Done")

    def save_output(self):
        logger.info("")
        data = plot.read_csv(self.parent.csv_filepath)
        self.finished.emit("Save: Done")
        return True


class UIRun(QMainWindow):
    def __init__(self, parent: "UIRunOptions", output_folder: str, model: Model, scenarios: List[Scenario],
                 options: dict, filters: dict):
        logger.info("")
        super().__init__()
        uic.loadUi("ui/run.ui", self)
        self.__child = None
        self.output_folder = os.path.join(output_folder, model.name)
        self.out_filepath = os.path.join(self.output_folder, "task.outx")
        self.csv_filepath = os.path.join(self.output_folder, "task.csv")
        self.model = model
        self.scenarios = scenarios
        self.options = options
        self.filters = filters

        self.current_index = None
        self.current_scenario = None

        self.parent = parent
        self.parent.hide()
        self.set_window()

        SystemManager.create_folder(self.output_folder)

        self.pb_run.clicked.connect(self.run_process)

    def set_window(self):
        logger.info("")
        self.lbl_model.setText(self.model.name)
        self.show()

    def set_text_to_default(self):
        logger.info("")
        self.lbl_initialize.setText("")
        self.lbl_channels.setText("")
        self.lbl_task.setText("")
        self.lbl_save.setText("")

    def run_process(self):
        logger.info("")
        for index, scenario in enumerate(self.scenarios):
            self.current_index = index
            self.current_scenario = scenario
            self.set_text_to_default()

            # Multithreading
            self.next_step("Run Process")

            # if not self.initialize(index, scenario):
            #     break
            # if not self.add_channels():
            #     break
            # if not self.run_task(scenario):
            #     break
            # if not self.save_output():
            #     break

    def next_step(self, msg: str):
        if msg == "Run Process":
            self.worker = Worker(self)
            self.worker.started.connect(self.worker.initialize)
            self.worker.finished.connect(self.next_step)
            self.worker.finished.connect(self.worker.quit)
            self.worker.start()
            self.lbl_initialize.setText("Running")
            self.lbl_scenario.setText(f"{self.current_scenario.name}   {self.current_index + 1}/{len(self.scenarios)}")
        elif msg.startswith("Initialize:"):
            if msg.endswith("Done"):
                self.lbl_initialize.setText("Done")
                self.worker2 = Worker(self)
                self.worker2.started.connect(self.worker2.add_channels)
                self.worker2.finished.connect(self.next_step)
                self.worker2.finished.connect(self.worker2.quit)
                self.worker2.start()
                self.lbl_channels.setText("Running")
            else:
                self.lbl_initialize.setText(msg)
        elif msg.startswith("Add Channels:"):
            if msg.endswith("Done"):
                self.lbl_channels.setText("Done")
                self.worker3 = Worker(self)
                self.worker3.started.connect(self.worker3.run_task)
                self.worker3.finished.connect(self.next_step)
                self.worker3.finished.connect(self.worker3.quit)
                self.worker3.start()
                self.lbl_task.setText("Running")
            else:
                self.lbl_channels.setText(msg)
        elif msg.startswith("Task:"):
            if msg.endswith("Done"):
                self.lbl_task.setText("Done")
                self.worker4 = Worker(self)
                self.worker4.started.connect(self.worker4.save_output)
                self.worker4.finished.connect(self.next_step)
                self.worker4.finished.connect(self.worker4.quit)
                self.worker4.start()
                self.lbl_save.setText("Running")
            else:
                self.lbl_task.setText(msg)
        elif msg.startswith("Save:"):
            if msg.endswith("Done"):
                self.lbl_save.setText("Done")
            else:
                self.lbl_save.setText(msg)

    def initialize(self, index: int, scenario: Scenario):
        logger.info("")
        self.lbl_scenario.setText(f"{scenario.name}   {index + 1}/{len(self.scenarios)}")
        functions = [(psse.initialize, None),
                     (psse.read_model_file, self.model.raw_path),
                     (psse.read_dynamics_file, self.model.dyr_path),
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
        busses = psse.read_bus_data(filters=self.filters)
        branches = psse.read_branch_data(filters=self.filters)
        for bus in busses.values():
            if self.options["bus_u"]:
                err_msg = psse.add_bus_u_channel(bus)
                if err_msg:
                    self.lbl_task.setText(f"Error: {err_msg}")
                    return False
        for branch in branches.values():
            if self.options["branch_p"]:
                err_msg = psse.add_branch_p_channel(branch)
                if err_msg:
                    self.lbl_task.setText(f"Error: {err_msg}")
                    return False
        return True

    def run_task(self, scenario: Scenario):
        logger.info("")
        self.lbl_task.setText("Running")

        err_msg = psse.initialize_output(self.out_filepath)
        if err_msg:
            self.lbl_task.setText(err_msg)
            return False

        for action in scenario.actions:
            action.activate()

        psse.save_output(self.out_filepath, self.csv_filepath)

        self.lbl_task.setText("Done")
        return True

    def save_output(self):
        logger.info("")
        self.lbl_save.setText("Running")

        data = plot.read_csv(self.csv_filepath)

        self.lbl_save.setText("Done")
        return True

    def closeEvent(self, event):
        logger.info("")
        self.parent.show()
        event.accept()
