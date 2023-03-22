import os
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6 import uic

from dsa.model import Model
from dsa.scenario import Scenario
from ui_py.ui_scenario import UIScenario
from ui_py.ui_message import UIMessage
from utils.logger import logger

if TYPE_CHECKING:
    from ui_py.ui_assessment import UIAssessment


class UIModel(QMainWindow):
    def __init__(self, parent: "UIAssessment", model: Model):
        logger.info("")
        super().__init__()
        uic.loadUi("ui/model.ui", self)
        self.__child = None
        self.model = model
        self.parent = parent
        self.message = None
        self.set_window()

        self.pb_raw.clicked.connect(self.__browse_raw)
        self.pb_dyr.clicked.connect(self.__browse_dyr)
        self.pb_add_new.clicked.connect(self.__add_new_scenario)
        self.pb_edit.clicked.connect(self.__edit_scenario)
        self.pb_remove.clicked.connect(self.__remove_scenario)
        self.pb_save.clicked.connect(self.__save)

    def __browse_raw(self):
        logger.info("")
        old_path = self.le_raw.text()
        filepath, _ = QFileDialog.getOpenFileName(self, 'Browse', filter='*.raw')
        self.le_raw.setText(filepath or old_path)

    def __browse_dyr(self):
        logger.info("")
        old_path = self.le_dyr.text()
        filepath, _ = QFileDialog.getOpenFileName(self, 'Browse', filter='*.dyr')
        self.le_dyr.setText(filepath or old_path)

    def __add_new_scenario(self):
        logger.info("")
        if not self.__check_raw():
            return
        scenario = Scenario()
        self.model.scenarios.append(scenario)
        self.__child = UIScenario(self, scenario)

    def __edit_scenario(self):
        logger.info("")
        if not self.__check_raw():
            return
        scenario_index = self.lw_scenarios.currentRow()
        if scenario_index >= 0:
            self.__child = UIScenario(self, self.model.scenarios[scenario_index])

    def __remove_scenario(self):
        logger.info("")
        scenario_index = self.lw_scenarios.currentRow()
        del self.model.scenarios[scenario_index]
        self.update_scenario_list()

    def __save(self):
        logger.info("")
        self.model.name = self.le_name.text()
        self.model.description = self.pte_description.toPlainText()
        self.model.raw_path = self.le_raw.text()
        self.model.dyr_path = self.le_dyr.text()
        self.close()

    def __check_raw(self):
        logger.info("")
        if not os.path.exists(self.le_raw.text()):
            self.message = UIMessage(self, "Warning!", "You need to select raw file!")
            self.message.show()
            return False
        return True

    def set_window(self):
        logger.info("")
        self.parent.hide()
        self.le_name.setText(self.model.name)
        self.pte_description.setPlainText(self.model.description)
        self.le_raw.setText(self.model.raw_path)
        self.le_dyr.setText(self.model.dyr_path)
        self.update_scenario_list()
        self.show()

    def update_scenario_list(self):
        logger.info("")
        self.lw_scenarios.clear()
        for scenario in self.model.scenarios:
            self.lw_scenarios.addItem(scenario.name)

    def closeEvent(self, event):
        logger.info("")
        self.parent.update_model_list()
        self.parent.show()
        event.accept()
