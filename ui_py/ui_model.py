from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6 import uic

from dsa.model import Model

if TYPE_CHECKING:
    from ui_py.ui_assessment import UIAssessment


class UIModel(QMainWindow):
    def __init__(self, parent: "UIAssessment", model: Model = None):
        super().__init__()
        uic.loadUi("ui/model.ui", self)
        self.__model = model
        self.parent = parent
        self.parent.hide()
        self.show()

        self.pb_raw.clicked.connect(self.__browse_raw)
        self.pb_dyr.clicked.connect(self.__browse_dyr)
        self.pb_save.clicked.connect(self.__save)

        if self.__model:
            self.__load_model()

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
        name = self.le_name.text()
        description = self.pte_description.toPlainText()
        raw = self.le_raw.text()
        dyr = self.le_dyr.text()
        model = Model(name=name, description=description, raw_path=raw, dyr_path=dyr)
        if self.__model:
            self.parent.update_model(model)
        else:
            self.parent.add_model(model)
        self.close()

    def __load_model(self):
        print("Loading existing model")
        self.le_name.setText(self.__model.name)
        self.pte_description.setPlainText(self.__model.description)
        self.le_raw.setText(self.__model.raw_path)
        self.le_dyr.setText(self.__model.dyr_path)

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.show()
        event.accept()
