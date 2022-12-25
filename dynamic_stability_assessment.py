from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6 import uic

from dsa.assessment import Assessment
from ui_py.ui_assessment import UIAssessment


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main_menu.ui", self)
        self.__child = None

        self.pb_create_assessment.clicked.connect(self.__create_assessment)
        self.pb_edit_assessment.clicked.connect(self.__edit_assessment)

    def __create_assessment(self):
        print("Creating New Assessment")
        assessment = Assessment()
        self.__child = UIAssessment(self, assessment)

    def __edit_assessment(self):
        print("Loading Assessment")
        filepath, _ = QFileDialog.getOpenFileName(self, 'Browse', filter='*.json')
        assessment = Assessment.load_from_json(filepath)
        self.__child = UIAssessment(self, assessment)

    def close_child_window(self):
        self.__child = None
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    window = MainMenu()
    window.show()
    app.exec()
