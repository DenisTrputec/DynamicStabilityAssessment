from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from dsa.scenario import Scenario

if TYPE_CHECKING:
    from ui_py.ui_model import UIModel


class UIScenario(QMainWindow):
    def __init__(self, parent: "UIModel", scenario: Scenario):
        super().__init__()
        uic.loadUi("ui/scenario.ui", self)
        self.__scenario = scenario
        self.parent = parent
        self.parent.hide()
        self.set_window()

        self.pb_edit.clicked.connect(self.__edit_action)
        self.pb_remove.clicked.connect(self.__remove_action)
        self.pb_simulation.clicked.connect(self.__simulation)
        self.pb_bus_fault.clicked.connect(self.__bus_fault)
        self.pb_line_fault.clicked.connect(self.__line_fault)
        self.pb_clear_fault.clicked.connect(self.__clear_fault)
        self.pb_trip_line.clicked.connect(self.__trip_line)
        self.pb_close_line.clicked.connect(self.__close_line)
        self.pb_disconnect_bus.clicked.connect(self.__disconnect_bus)
        self.pb_disconnect_machine.clicked.connect(self.__disconnect_machine)
        self.pb_save.clicked.connect(self.__save)

    def __edit_action(self):
        print("Editing Action")

    def __remove_action(self):
        print("Removing Action")

    def __simulation(self):
        print("Add Perform Simulation")

    def __bus_fault(self):
        print("Add Bus Fault")

    def __line_fault(self):
        print("Add Line Fault")

    def __clear_fault(self):
        print("Add Clear Fault")

    def __trip_line(self):
        print("Add Trip Line")

    def __close_line(self):
        print("Add Close Line")

    def __disconnect_bus(self):
        print("Add Disconnect Bus")

    def __disconnect_machine(self):
        print("Add Disconnect Machine")

    def __save(self):
        print("Saving new Model")
        self.__scenario.name = self.le_name.text()
        self.__scenario.description = self.pte_description.toPlainText()
        self.close()

    def set_window(self):
        print("Setting Model Window")
        self.le_name.setText(self.__scenario.name)
        self.pte_description.setPlainText(self.__scenario.description)
        self.show()

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        # self.parent.update_model_list()
        self.parent.show()
        event.accept()