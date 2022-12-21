from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6 import uic

from dsa.model import Model

if TYPE_CHECKING:
    from py_ui.create_assessment import CreateAssessment


class CreateModel(QMainWindow):
    def __init__(self, parent: "CreateAssessment"):
        super().__init__()
        uic.loadUi("ui/create_model.ui", self)
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
        name = self.le_name.text()
        description = self.pte_description.toPlainText()
        raw = self.le_raw.text()
        dyr = self.le_dyr.text()
        model = Model(name=name, description=description, raw_path=raw, dyr_path=dyr)
        self.parent.add_model(model)
        self.close()

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.show()
        event.accept()
