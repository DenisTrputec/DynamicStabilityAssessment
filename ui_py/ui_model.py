import os
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6 import uic

from dsa.model import Model
from dsa.scenario import Scenario
from ui_py.ui_scenario import UIScenario
from ui_py.ui_message import UIMessage

if TYPE_CHECKING:
    from ui_py.ui_assessment import UIAssessment


class UIModel(QMainWindow):
    def __init__(self, parent: "UIAssessment", model: Model):
        super().__init__()
        uic.loadUi("ui/model.ui", self)
        self.__model = model
        self.parent = parent
        self.parent.hide()
        self.message = None
        self.set_window()

        self.pb_raw.clicked.connect(self.__browse_raw)
        self.pb_dyr.clicked.connect(self.__browse_dyr)
        self.pb_add_new.clicked.connect(self.__add_new_scenario)
        self.pb_edit.clicked.connect(self.__edit_scenario)
        self.pb_remove.clicked.connect(self.__remove_scenario)
        self.pb_save.clicked.connect(self.__save)

    def __browse_raw(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Browse', filter='*.raw')
        self.le_raw.setText(filepath)
        print("Browsing for RAW")

    def __browse_dyr(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Browse', filter='*.dyr')
        self.le_dyr.setText(filepath)
        print("Browsing for DYR")

    def __add_new_scenario(self):
        print("Adding New Scenario")
        if not self.__check_raw():
            return
        scenario = Scenario()
        self.__model.scenarios.append(scenario)
        self.__child = UIScenario(self, scenario)

    def __edit_scenario(self):
        print("Editing Model")
        if not self.__check_raw():
            return
        row_number = self.lw_models.currentRow()
        if row_number >= 0:
            self.__child = UIScenario(self, self.__model.scenarios[row_number])

    def __remove_scenario(self):
        print("Removing Model")

    def __save(self):
        print("Saving new Model")
        self.__model.name = self.le_name.text()
        self.__model.description = self.pte_description.toPlainText()
        self.__model.raw_path = self.le_raw.text()
        self.__model.dyr_path = self.le_dyr.text()
        self.close()

    def __check_raw(self):
        if not os.path.exists(self.le_raw.text()):
            self.message = UIMessage(self, "Warning!", "You need to select raw file!")
            self.message.show()
            return False
        return True

    def set_window(self):
        print("Setting Model Window")
        self.le_name.setText(self.__model.name)
        self.pte_description.setPlainText(self.__model.description)
        self.le_raw.setText(self.__model.raw_path)
        self.le_dyr.setText(self.__model.dyr_path)
        self.show()

    def update_scenario_list(self):
        self.lw_scenarios.clear()
        for scenario in self.__model.scenarios:
            self.lw_scenarios.addItem(scenario.name)

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.update_model_list()
        self.parent.show()
        event.accept()
