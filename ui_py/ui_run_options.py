from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QCheckBox
from PyQt6 import uic

from dsa.assessment import Assessment
from dsa.model import Model
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
        self.run_list = []

        self.parent = parent
        self.parent.hide()
        self.set_window()

        self.pb_back.clicked.connect(self.__back)

    def __back(self):
        self.close()

    def __update_checkboxes(self, model: Model):
        vbox = QVBoxLayout()
        self.gb_scenarios.setLayout(vbox)
        checkbox = QCheckBox("Select All")
        checkbox.stateChanged.connect(self.__select_all)
        vbox.addWidget(checkbox)
        for scenario in model.scenarios:
            checkbox = QCheckBox(scenario.name)
            checkbox.setProperty(scenario.name, scenario)
            vbox.addWidget(checkbox)

    def __select_all(self):
        for checkbox in self.gb_scenarios.findChildren(QCheckBox):
            checkbox.setChecked(True)

    def set_window(self):
        logger.info("")
        for model in self.__assessment.models:
            self.cb_models.addItem(model.name, model)
        self.__update_checkboxes(self.cb_models.currentData())
        self.show()

    def closeEvent(self, event):
        logger.info(f"")
        self.parent.close_child_window()
        event.accept()
