from typing import TYPE_CHECKING, List, Union

from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

from power_system.bus import Bus
from power_system.branch import Branch
from power_system.machine import Machine
from dsa.action import Action

if TYPE_CHECKING:
    from ui_py.ui_scenario import UIScenario


class UIPickElement(QDialog):
    def __init__(self, parent: "UIScenario", name: str, elements: List[Union[Bus, Branch, Machine]], method_key: str,
                 action: Action = None):
        super().__init__()
        uic.loadUi("ui/element_picker.ui", self)
        self.parent = parent
        self.__name = name
        self.__method_key = method_key
        self.__elements = elements
        self.__action = action
        self.set_window()

        self.pb_ok.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        element = self.cb_elements.currentData()
        if not element:
            self.close()
        if self.__action:
            self.__action.argument = element
            self.__action.update_name()
            self.parent.scenario.update_corresponding_clear_fault(self.__action)
        else:
            action = Action(self.__name, self.__method_key, element)
            self.parent.scenario.actions.append(action)
        self.parent.scenario.update_clear_faults_indexes()
        self.close()

    def set_window(self):
        self.lbl_title.setText(self.__name)
        for index, element in enumerate(self.__elements):
            self.cb_elements.addItem(element.full_name, element)
            if self.__action and self.__action.argument.name == element.name:
                self.cb_elements.setCurrentIndex(index)
        self.show()

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.update_action_list()
        event.accept()
