from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from dsa.assessment import Assessment
from dsa.model import Model
from ui_py.ui_model import UIModel
from utils.logger import logger

if TYPE_CHECKING:
    from dynamic_stability_assessment import MainMenu


class UIAssessment(QMainWindow):
    def __init__(self, parent: "MainMenu", assessment: Assessment):
        logger.info("")
        super().__init__()
        uic.loadUi("ui/assessment.ui", self)
        self.__models = []

        self.parent = parent
        self.assessment = assessment
        self.child = None

        self.pb_add_new.clicked.connect(self.__add_new_model)
        self.pb_edit.clicked.connect(self.__edit_model)
        self.pb_remove.clicked.connect(self.__remove_model)
        self.pb_save.clicked.connect(self.__save)
        self.pb_back.clicked.connect(self.__back)

        self.set_window()

    def __add_new_model(self):
        logger.info("")
        model = Model()
        self.assessment.models.append(model)
        self.child = UIModel(self, model, is_new=True)

    def __edit_model(self):
        logger.info("")
        row_number = self.lw_models.currentRow()
        if row_number >= 0:
            self.child = UIModel(self, self.assessment.models[row_number])

    def __remove_model(self):
        logger.info("")
        model_index = self.lw_models.currentRow()
        del self.assessment.models[model_index]
        self.update_model_list()

    def __save(self):
        logger.info("")
        self.assessment.name = self.le_name.text()
        self.assessment.description = self.pte_description.toPlainText()
        self.assessment.save()
        self.close()

    def __back(self):
        logger.info("")
        self.close()

    def set_window(self):
        logger.info("")
        self.parent.hide()
        self.le_name.setText(self.assessment.name)
        self.pte_description.setPlainText(self.assessment.description)
        self.update_model_list()
        self.show()

    def update_model_list(self):
        logger.info("")
        self.lw_models.clear()
        for model in self.assessment.models:
            self.lw_models.addItem(model.name)

    def add_model(self, model):
        logger.info("")
        self.assessment.models.append(model)
        self.lw_models.addItem(model.name)

    def update_model(self, model):
        logger.info("")
        row_number = self.lw_models.currentRow()
        self.assessment.models[row_number] = model
        self.lw_models.takeItem(row_number)
        self.lw_models.insertItem(row_number, model.name)

    def closeEvent(self, event):
        logger.info("")
        self.parent.child = None
        self.parent.show()
        event.accept()
