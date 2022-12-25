from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from dsa.assessment import Assessment
from ui_py.ui_model import UIModel

if TYPE_CHECKING:
    from dynamic_stability_assessment import MainMenu


class UIAssessment(QMainWindow):
    def __init__(self, parent: "MainMenu", assessment: Assessment = None):
        super().__init__()
        uic.loadUi("ui/assessment.ui", self)
        self.__assessment = assessment
        self.__child = None
        self.__models = []

        self.parent = parent
        self.parent.hide()
        self.show()

        self.pb_add_new.clicked.connect(self.__add_new)
        self.pb_edit.clicked.connect(self.__edit)
        self.pb_remove.clicked.connect(self.__remove)
        self.pb_save.clicked.connect(self.__save)

        if assessment:
            self.__load_assessment()

    def __load_assessment(self):
        print("Loading existing model")
        self.le_name.setText(self.__assessment.name)
        self.pte_description.setPlainText(self.__assessment.description)

    def __add_new(self):
        print("Adding New Model")
        self.__child = UIModel(self)

    def __edit(self):
        print("Editing Model")
        row_number = self.lw_models.currentRow()
        if row_number > 0:
            self.__child = UIModel(self, self.__models[row_number])

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

    def update_model(self, model):
        print("Updating model in list")
        row_number = self.lw_models.currentRow()
        self.__models[row_number] = model
        self.lw_models.takeItem(row_number)
        self.lw_models.insertItem(row_number, model.name)

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.close_child_window()
        event.accept()
