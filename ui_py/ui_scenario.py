from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from dsa.scenario import Scenario
from dsa.psse import PSSE
from ui_py.ui_pick_element import UIPickElement

if TYPE_CHECKING:
    from ui_py.ui_model import UIModel


class UIScenario(QMainWindow):
    def __init__(self, parent: "UIModel", scenario: Scenario):
        super().__init__()
        uic.loadUi("ui/scenario.ui", self)
        self.__child = None
        self.scenario = scenario
        self.parent = parent
        self.parent.hide()
        self.set_window()

        PSSE.initialize()
        PSSE.read_raw(self.parent.le_raw.text())
        self.buses = PSSE.read_busses()
        self.branches = PSSE.read_branches(self.buses)
        self.machines = PSSE.read_machines(self.buses)

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
        self.__child = UIPickElement(self, "Bus Fault", self.buses, "bus_fault")

    def __line_fault(self):
        print("Add Line Fault")
        self.__child = UIPickElement(self, "Line Fault", self.branches, "line_fault")

    def __clear_fault(self):
        print("Add Clear Fault")

    def __trip_line(self):
        print("Add Trip Line")
        self.__child = UIPickElement(self, "Trip Line", self.branches, "line_trip")

    def __close_line(self):
        print("Add Close Line")
        self.__child = UIPickElement(self, "Close Line", self.branches, "line_close")

    def __disconnect_bus(self):
        print("Add Disconnect Bus")
        self.__child = UIPickElement(self, "Disconnect Bus", self.buses, "bus_disconnect")

    def __disconnect_machine(self):
        print("Add Disconnect Machine")
        self.__child = UIPickElement(self, "Disconnect Machine", self.machines, "machine_disconnect")

    def __save(self):
        print("Saving new Model")
        self.scenario.name = self.le_name.text()
        self.scenario.description = self.pte_description.toPlainText()
        self.close()

    def set_window(self):
        print("Setting Model Window")
        self.le_name.setText(self.scenario.name)
        self.pte_description.setPlainText(self.scenario.description)
        self.update_action_list()
        self.show()

    def update_action_list(self):
        self.lw_actions.clear()
        for action in self.scenario.actions:
            self.lw_actions.addItem(action.name)

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.update_scenario_list()
        self.parent.show()
        event.accept()
