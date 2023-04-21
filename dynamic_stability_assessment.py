from os.path import exists

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6 import uic

from dsa.assessment import Assessment
from ui_py.ui_assessment import UIAssessment
from ui_py.ui_run_options import UIRunOptions
from utils.logger import logger


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main_menu.ui", self)

        self.child = None

        self.pb_create_assessment.clicked.connect(self.__create_assessment)
        self.pb_edit_assessment.clicked.connect(self.__edit_assessment)
        self.pb_run_assessment.clicked.connect(self.__run_assessment)
        self.pb_quit.clicked.connect(self.__quit)

    def __create_assessment(self):
        logger.info("")
        assessment = Assessment()
        self.child = UIAssessment(self, assessment)

    def __edit_assessment(self):
        logger.info("")
        filepath, _ = QFileDialog.getOpenFileName(self, 'Browse', filter='*.json')
        if not exists(filepath):
            return
        assessment = Assessment.load_from_json(filepath)
        self.child = UIAssessment(self, assessment)

    def __run_assessment(self):
        logger.info("")
        filepath, _ = QFileDialog.getOpenFileName(self, 'Browse', filter='*.json')
        if not exists(filepath):
            return
        assessment = Assessment.load_from_json(filepath)
        self.child = UIRunOptions(self, assessment)

    def __quit(self):
        logger.info("")
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = MainMenu()
    window.show()
    app.exec()
