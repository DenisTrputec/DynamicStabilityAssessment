from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QCheckBox, QFileDialog, QLineEdit
from PyQt6 import uic

from dsa.assessment import Assessment
from dsa.model import Model
from ui_py.ui_run import UIRun
from utils.logger import logger

if TYPE_CHECKING:
    from dynamic_stability_assessment import MainMenu


class UIRunOptions(QMainWindow):
    def __init__(self, parent: "MainMenu", assessment: Assessment):
        logger.info("")
        super().__init__()
        uic.loadUi("ui/run_options.ui", self)
        self.__child = None
        self.__assessment = assessment

        self.parent = parent
        self.parent.hide()
        self.set_window()

        self.pb_back.clicked.connect(self.__back)
        self.pb_output.clicked.connect(self.__browse)
        self.pb_run.clicked.connect(self.__run)

    def __back(self):
        logger.info("")
        self.close()

    def __browse(self):
        logger.info("")
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.le_output.setText(folder_path)

    def __update_checkboxes(self, model: Model):
        logger.info("")
        vbox = QVBoxLayout()
        self.gb_scenarios.setLayout(vbox)
        checkbox = QCheckBox("Select All")
        checkbox.stateChanged.connect(self.__select_all)
        vbox.addWidget(checkbox)
        for scenario in model.scenarios:
            checkbox = QCheckBox(scenario.name)
            checkbox.setProperty("scenario", scenario)
            vbox.addWidget(checkbox)

    def __select_all(self):
        logger.info("")
        for checkbox in self.gb_scenarios.findChildren(QCheckBox):
            checkbox.setChecked(True)

    def __run(self):
        logger.info("")
        output_folder = self.le_output.text()
        model = self.cb_models.currentData()

        scenarios_to_run = []
        for checkbox in self.gb_scenarios.findChildren(QCheckBox):
            if checkbox.isChecked():
                if checkbox.property("scenario"):
                    scenarios_to_run.append(checkbox.property("scenario"))

        options = {"branch_p": False, "bus_u": False}
        for checkbox, option_key in zip(self.gb_options.findChildren(QCheckBox), options):
            if checkbox.isChecked():
                options[option_key] = True

        filters = {"area": []}
        for line_edit, filter_key in zip(self.gb_options.findChildren(QLineEdit), filters):
            values = line_edit.text().split(',')
            try:
                filters[filter_key] = [int(v.strip()) for v in values]
            except ValueError:
                pass
        self.__child = UIRun(self, output_folder, model, scenarios_to_run, options, filters)

    def set_window(self):
        logger.info("")
        for model in self.__assessment.models:
            self.cb_models.addItem(model.name, model)
        self.__update_checkboxes(self.cb_models.currentData())
        self.show()

    def closeEvent(self, event):
        logger.info(f"")
        self.parent.show()
        event.accept()
