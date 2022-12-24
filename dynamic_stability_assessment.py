from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

from ui_py.ui_assessment import UIAssessment


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main_menu.ui", self)
        self.__child = None

        self.pb_create_assessment.clicked.connect(self.__create_assessment)
        self.pb_load_assessment.clicked.connect(self.__load_assessment)

    def __create_assessment(self):
        print("Creating New Assessment")
        self.__child = UIAssessment(self)

    def __load_assessment(self):
        print("Loading Assessment")

    def close_child_window(self):
        self.__child = None
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    window = MainMenu()
    window.show()
    app.exec()
