from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

if TYPE_CHECKING:
    from ui_py.ui_model import UIModel


class UIMessage(QDialog):
    def __init__(self, parent, title: str, text: str):
        super().__init__()
        uic.loadUi("ui/message.ui", self)
        self.parent = parent

        self.lbl_title.setText(title)
        self.lbl_text.setText(text)

        self.pb_ok.clicked.connect(self.close)

    def closeEvent(self, event):
        print(f"Closing {self.__class__.__name__}")
        self.parent.message = None
        event.accept()
