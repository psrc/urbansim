# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from gui.file_menu.dbconnection_page import DBConnectionPage

class DBConnectionDialog(QWizard):
    def __init__(self, project, parent=None):
        super(DBConnectionDialog, self).__init__(parent)

        self.project = project

        self.setWindowTitle("Data Source Connection")
        self.setWindowIcon(QIcon("./images/datasource.png"))

        self.setWizardStyle(QWizard.ClassicStyle)
        self.setOption(QWizard.NoBackButtonOnStartPage)

        self.connectionPage = DBConnectionPage()
        self.connectionPage.usernameLineEdit.setText(self.project.db.username)
        self.connectionPage.hostnameLineEdit.setText(self.project.db.hostname)
        self.connectionPage.passwordLineEdit.setText(self.project.db.password)

        self.addPage(self.connectionPage)

    def accept(self):
        self.project.db.username = self.connectionPage.usernameLineEdit.text()
        self.project.db.hostname = self.connectionPage.hostnameLineEdit.text()
        self.project.db.password = self.connectionPage.passwordLineEdit.text()

        QWizard.accept(self)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    project = "project"

    dia = DbConnectionDialog(project)
    dia.show()
    app.exec_()
