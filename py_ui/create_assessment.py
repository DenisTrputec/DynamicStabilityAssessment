from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic


class CreateAssessment(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("ui/create_assessment.ui", self)
        self.parent = parent
        self.parent.hide()
        self.show()

    def closeEvent(self, event):
        self.parent.show()
        event.accept()
