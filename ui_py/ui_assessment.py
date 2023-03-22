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
        self.__child = None
        self.__assessment = assessment
        self.__models = []

        self.parent = parent
        self.parent.hide()
        self.set_window()

        self.pb_add_new.clicked.connect(self.__add_new_model)
        self.pb_edit.clicked.connect(self.__edit_model)
        self.pb_remove.clicked.connect(self.__remove_model)
        self.pb_save.clicked.connect(self.__save)

    def __add_new_model(self):
        logger.info("")
        model = Model()
        self.__assessment.models.append(model)
        self.__child = UIModel(self, model)

    def __edit_model(self):
        logger.info("")
        row_number = self.lw_models.currentRow()
        if row_number >= 0:
            self.__child = UIModel(self, self.__assessment.models[row_number])

    def __remove_model(self):
        logger.info("")
        model_index = self.lw_models.currentRow()
        del self.__assessment.models[model_index]
        self.update_model_list()

    def __save(self):
        logger.info("")
        self.__assessment.name = self.le_name.text()
        self.__assessment.description = self.pte_description.toPlainText()
        self.__assessment.save()
        self.close()

    def set_window(self):
        logger.info("")
        self.le_name.setText(self.__assessment.name)
        self.pte_description.setPlainText(self.__assessment.description)
        self.update_model_list()
        self.show()

    def update_model_list(self):
        logger.info("")
        self.lw_models.clear()
        for model in self.__assessment.models:
            self.lw_models.addItem(model.name)

    def add_model(self, model):
        logger.info("")
        self.__assessment.models.append(model)
        self.lw_models.addItem(model.name)

    def update_model(self, model):
        logger.info("")
        row_number = self.lw_models.currentRow()
        self.__assessment.models[row_number] = model
        self.lw_models.takeItem(row_number)
        self.lw_models.insertItem(row_number, model.name)

    def closeEvent(self, event):
        logger.info(f"")
        self.parent.close_child_window()
        event.accept()
