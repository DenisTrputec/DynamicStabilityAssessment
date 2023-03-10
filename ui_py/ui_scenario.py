from typing import TYPE_CHECKING, List, Union

from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from dsa.scenario import Scenario
from dsa.psse import PSSE
from ui_py.ui_pick_element import UIPickElement
from ui_py.ui_pick_value import UIPickValue

if TYPE_CHECKING:
    from ui_py.ui_model import UIModel
    from power_system.bus import Bus
    from power_system.branch import Branch
    from power_system.machine import Machine


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
        self.pb_move_up.clicked.connect(self.__move_up)
        self.pb_move_down.clicked.connect(self.__move_down)
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
        index = self.lw_actions.currentRow()
        action = self.scenario.actions[index]
        if action.method_key == "simulation":
            self.__child = UIPickValue(self, "Simulation", "simulation", action)
        elif action.method_key == "bus_fault":
            buses = [action.argument] + self.available_elements(self.buses, "bus_fault")
            self.__child = UIPickElement(self, "Bus Fault", buses, "bus_fault", action)
        elif action.method_key == "line_fault":
            branches = [action.argument] + self.available_elements(self.branches, "line_fault")
            self.__child = UIPickElement(self, "Line Fault", branches, "line_fault", action)
        elif action.method_key == "clear_fault":
            self.clears = [action.argument.name for action in self.scenario.actions if
                           action.method_key == "clear_fault"]
            self.faults = [action.argument for action in self.scenario.actions[:index]
                           if action.method_key in ["bus_fault", "line_fault"]
                           and action.argument.name not in self.clears]
            self.faults = [action.argument] + self.faults
            self.__child = UIPickElement(self, "Clear Fault", self.faults, "clear_fault", action)
        self.update_action_list()

    def __remove_action(self):
        print("Removing Action")
        action_index = self.lw_actions.currentRow()
        clear_index = self.__return_corresponding_clear_fault_index(action_index)
        if clear_index:
            del self.scenario.actions[clear_index]
        del self.scenario.actions[action_index]
        self.scenario.update_clear_faults_indexes()
        self.update_action_list()

    def __move_up(self):
        i = self.lw_actions.currentRow()
        if i > 0:
            self.scenario.actions[i - 1], self.scenario.actions[i] = \
                self.scenario.actions[i], self.scenario.actions[i - 1]
        self.scenario.update_clear_faults_indexes()
        self.update_action_list()

    def __move_down(self):
        i = self.lw_actions.currentRow()
        if i + 1 < len(self.scenario.actions):
            self.scenario.actions[i], self.scenario.actions[i + 1] = \
                self.scenario.actions[i + 1], self.scenario.actions[i]
        self.scenario.update_clear_faults_indexes()
        self.update_action_list()

    def __simulation(self):
        print("Add Perform Simulation")
        self.__child = UIPickValue(self, "Simulation", "simulation")

    def __bus_fault(self):
        print("Add Bus Fault")
        buses = self.available_elements(self.buses, "bus_fault")
        self.__child = UIPickElement(self, "Bus Fault", buses, "bus_fault")

    def __line_fault(self):
        print("Add Line Fault")
        branches = self.available_elements(self.branches, "line_fault")
        self.__child = UIPickElement(self, "Line Fault", branches, "line_fault")

    def __clear_fault(self):
        print("Add Clear Fault")
        self.clears = [action.argument.name for action in self.scenario.actions if action.method_key == "clear_fault"]
        self.faults = [action.argument for action in self.scenario.actions
                       if action.method_key in ["bus_fault", "line_fault"]
                       and action.argument.name not in self.clears]
        self.__child = UIPickElement(self, "Clear Fault", self.faults, "clear_fault")

    def __trip_line(self):
        print("Add Trip Line")
        branches = self.available_elements(self.branches, "line_trip")
        self.__child = UIPickElement(self, "Trip Line", branches, "line_trip")

    def __close_line(self):
        print("Add Close Line")
        branches = self.available_elements(self.branches, "line_close")
        self.__child = UIPickElement(self, "Close Line", branches, "line_close")

    def __disconnect_bus(self):
        print("Add Disconnect Bus")
        buses = self.available_elements(self.buses, "bus_disconnect")
        self.__child = UIPickElement(self, "Disconnect Bus", buses, "bus_disconnect")

    def __disconnect_machine(self):
        print("Add Disconnect Machine")
        machines = self.available_elements(self.machines, "machine_disconnect")
        self.__child = UIPickElement(self, "Disconnect Machine", machines, "machine_disconnect")

    def __save(self):
        print("Saving new Model")
        self.scenario.name = self.le_name.text()
        self.scenario.description = self.pte_description.toPlainText()
        self.close()

    def __return_corresponding_clear_fault_index(self, index: int):
        # if bus_fault or line_fault delete also corresponding clear_fault
        if self.scenario.actions[index].method_key in ["bus_fault", "line_fault"]:
            fault_name = self.scenario.actions[index].argument.name
            for clear_index, action in enumerate(self.scenario.actions[index + 1:]):
                if action.method_key == "clear_fault" and action.argument.name == fault_name:
                    return index + clear_index + 1
        return None

    def available_elements(self, elements: List[Union["Bus", "Branch", "Machine"]], method_string: str):
        used = [action.argument.name for action in self.scenario.actions if action.method_key == method_string]
        return [b for b in elements if b.name not in used]

    def set_window(self):
        print("Setting Model Window")
        self.le_name.setText(self.scenario.name)
        self.pte_description.setPlainText(self.scenario.description)
        self.update_action_list()
        self.show()

    def update_action_list(self):
        print("Updating Action List")
        self.lw_actions.clear()
        for action in self.scenario.actions:
            self.lw_actions.addItem(action.name)

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.update_scenario_list()
        self.parent.show()
        event.accept()
