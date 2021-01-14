# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import QLineEdit, QPushButton

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from controller.LoginController import LoginController as controller
from database.connection import connection


class main(QWidget):
    def __init__(self):
        super(main, self).__init__()
        self.controller = controller(conn=connection())
        self.load_ui()
        self.set_widgets()

    def set_widgets(self):
        self.btnWidgetLogin: QPushButton = self.ui.btnLogin
        self.usernameWidget: QLineEdit = self.ui.lineUsername
        self.passwordWidget: QLineEdit = self.ui.linePass
        self.btnWidgetLogin.clicked.connect(
            lambda: self.controller.log_in(username=self.usernameWidget.text(), password=self.passwordWidget.text(),
                                           loginUi=self))

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "views/login.ui")
        print(os.path.dirname(__file__), "login.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = main()
    widget.show()
    sys.exit(app.exec_())
