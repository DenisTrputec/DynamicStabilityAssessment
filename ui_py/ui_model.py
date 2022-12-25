from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6 import uic

from dsa.model import Model

if TYPE_CHECKING:
    from ui_py.ui_assessment import UIAssessment


class UIModel(QMainWindow):
    def __init__(self, parent: "UIAssessment", model: Model):
        super().__init__()
        uic.loadUi("ui/model.ui", self)
        self.__model = model
        self.parent = parent
        self.parent.hide()
        self.show()

        self.pb_raw.clicked.connect(self.__browse_raw)
        self.pb_dyr.clicked.connect(self.__browse_dyr)
        self.pb_save.clicked.connect(self.__save)

    def __browse_raw(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Browse', filter='*.raw')
        self.le_raw.setText(filepath)
        print("Browsing for RAW")

    def __browse_dyr(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Browse', filter='*.dyr')
        self.le_dyr.setText(filepath)
        print("Browsing for DYR")

    def __save(self):
        print("Saving new Model")
        self.__model.name = self.le_name.text()
        self.__model.description = self.pte_description.toPlainText()
        self.__model.raw = self.le_raw.text()
        self.__model.dyr = self.le_dyr.text()
        self.close()

    def set_window(self):
        print("Setting Model Window")
        self.le_name.setText(self.__model.name)
        self.pte_description.setPlainText(self.__model.description)
        self.le_raw.setText(self.__model.raw_path)
        self.le_dyr.setText(self.__model.dyr_path)

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.update_model_list()
        self.parent.show()
        event.accept()
