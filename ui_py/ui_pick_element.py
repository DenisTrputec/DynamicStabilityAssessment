from typing import TYPE_CHECKING, Callable, List, Union

from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

from power_system.bus import Bus
from power_system.branch import Branch
from power_system.machine import Machine
from dsa.action import Action

if TYPE_CHECKING:
    from ui_py.ui_model import UIModel


class UIPickElement(QDialog):
    def __init__(self, parent, name: str, elements: List[Union[Bus, Branch, Machine]], method_key: str):
        super().__init__()
        uic.loadUi("ui/element_picker.ui", self)
        self.parent = parent
        self.__name = name
        self.__method_key = method_key
        self.__elements = elements
        self.set_window()

        self.pb_ok.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        element = self.cb_elements.currentData()
        action = Action(self.__name, self.__method_key, element)
        self.parent.scenario.actions.append(action)
        self.close()

    def set_window(self):
        self.lbl_title.setText(self.__name)
        for element in self.__elements:
            self.cb_elements.addItem(element.full_name, element)
        self.show()

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.update_action_list()
        self.parent.message = None
        event.accept()
