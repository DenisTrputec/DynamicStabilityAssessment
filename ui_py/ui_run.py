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
                else:
                    self.parent.channels.append(bus)
        for branch in branches.values():
            if self.parent.options["branch_p"]:
                err_msg = psse.add_branch_p_channel(branch)
                if err_msg:
                    self.finished.emit("Add Channels: " + err_msg)
                else:
                    self.parent.channels.append(branch)
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
        # data_400 = plot.filter_data(data, self.parent.channels, "voltage_level")
        # plot.plot_figure(data.iloc[:, 0], "x", [data_400], ["y400"], "E:\\Python3\\DynamicStabilityAssessment\\output\\test.png", "Naslov")
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
        self.channels = []

        self.current_index = None
        self.current_scenario = None

        self.parent = parent
        self.parent.hide()
        self.set_window()

        SystemManager.create_folder(self.output_folder)

        self.pb_back.clicked.connect(self.__back)
        self.pb_run.clicked.connect(self.run_process)

    def __back(self):
        logger.info("")
        self.close()

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
        self.current_index = 0
        self.first_step()

    def first_step(self):
        logger.info("")
        self.current_scenario = self.scenarios[self.current_index]
        self.set_text_to_default()
        self.next_step("Run Process")

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
                if self.current_index < len(self.scenarios) - 1:
                    self.current_index += 1
                    self.first_step()
                else:
                    self.pb_run.setEnabled(False)
            else:
                self.lbl_save.setText(msg)

    def closeEvent(self, event):
        logger.info("")
        self.parent.show()
        event.accept()
