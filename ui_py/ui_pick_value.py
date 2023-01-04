from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

from dsa.action import Action

if TYPE_CHECKING:
    from ui_py.ui_scenario import UIScenario


class UIPickValue(QDialog):
    def __init__(self, parent: "UIScenario", name: str, method_key: str, action: Action = None):
        super().__init__()
        uic.loadUi("ui/value_picker.ui", self)
        self.parent = parent
        self.__name = name
        self.__method_key = method_key
        self.__action = action
        self.set_window()

        self.pb_ok.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        value = float(self.le_value.text())
        if self.__action:
            self.__action.argument = value
            self.__action.update_name()
        else:
            action = Action(self.__name, self.__method_key, value)
            self.parent.scenario.actions.append(action)
        self.close()

    def set_window(self):
        self.lbl_title.setText(self.__name)
        if self.__action:
            self.le_value.setText(str(self.__action.argument))
        else:
            self.le_value.setText("")
        self.show()

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.update_action_list()
        event.accept()
