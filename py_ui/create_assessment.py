from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
from PyQt6 import uic

from dsa.assessment import Assessment
from py_ui.create_model import CreateModel

if TYPE_CHECKING:
    from dynamic_stability_assessment import MainMenu


class CreateAssessment(QMainWindow):
    def __init__(self, parent: "MainMenu"):
        super().__init__()
        uic.loadUi("ui/create_assessment.ui", self)
        self.__child = None
        self.__models = []
        self.parent = parent
        self.parent.hide()
        self.show()

        self.pb_add_new.clicked.connect(self.__add_new)
        self.pb_edit.clicked.connect(self.__edit)
        self.pb_remove.clicked.connect(self.__remove)
        self.pb_save.clicked.connect(self.__save)

    def __add_new(self):
        print("Adding New Model")
        self.__child = CreateModel(self)

    def __edit(self):
        print("Editing Model")

    def __remove(self):
        print("Removing Model")

    def __save(self):
        print(f"Saving... {self}")
        name = self.le_name.text()
        description = self.pte_description.toPlainText()
        assessment = Assessment(name=name, description=description, models=self.__models)
        assessment.save()
        self.close()

    def add_model(self, model):
        print("Adding model to list")
        self.__models.append(model)
        self.lw_models.addItem(model.name)

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.show()
        event.accept()
