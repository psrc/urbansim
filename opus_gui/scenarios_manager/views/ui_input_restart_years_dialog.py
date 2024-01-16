# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input_restart_years_dialog.ui'
#
# Created: Sat May  7 17:20:47 2011
#      by: PyQt5 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_dlgInputRestartYears(object):
    def setupUi(self, dlgInputRestartYears):
        dlgInputRestartYears.setObjectName("dlgInputRestartYears")
        dlgInputRestartYears.resize(413, 140)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgInputRestartYears)
        self.buttonBox.setGeometry(QtCore.QRect(60, 97, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.leFirstYear = QtWidgets.QLineEdit(dlgInputRestartYears)
        self.leFirstYear.setGeometry(QtCore.QRect(213, 52, 81, 25))
        self.leFirstYear.setObjectName("leFirstYear")
        self.leLastYear = QtWidgets.QLineEdit(dlgInputRestartYears)
        self.leLastYear.setGeometry(QtCore.QRect(307, 52, 81, 25))
        self.leLastYear.setObjectName("leLastYear")
        self.label_2 = QtWidgets.QLabel(dlgInputRestartYears)
        self.label_2.setGeometry(QtCore.QRect(213, 29, 63, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(dlgInputRestartYears)
        self.label_3.setGeometry(QtCore.QRect(307, 29, 62, 17))
        self.label_3.setObjectName("label_3")
        self.lblEndYear = QtWidgets.QLabel(dlgInputRestartYears)
        self.lblEndYear.setGeometry(QtCore.QRect(118, 53, 81, 25))
        self.lblEndYear.setText("")
        self.lblEndYear.setObjectName("lblEndYear")
        self.label = QtWidgets.QLabel(dlgInputRestartYears)
        self.label.setGeometry(QtCore.QRect(118, 29, 57, 17))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(dlgInputRestartYears)
        self.label_4.setGeometry(QtCore.QRect(25, 29, 65, 17))
        self.label_4.setObjectName("label_4")
        self.lblBaseYear = QtWidgets.QLabel(dlgInputRestartYears)
        self.lblBaseYear.setGeometry(QtCore.QRect(25, 53, 81, 25))
        self.lblBaseYear.setText("")
        self.lblBaseYear.setObjectName("lblBaseYear")

        self.retranslateUi(dlgInputRestartYears)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("accepted()"), dlgInputRestartYears.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("rejected()"), dlgInputRestartYears.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgInputRestartYears)

    def retranslateUi(self, dlgInputRestartYears):
        dlgInputRestartYears.setWindowTitle(QtWidgets.QApplication.translate("dlgInputRestartYears", "The First and Last Year of Restart Run", None))
        self.leFirstYear.setToolTip(QtWidgets.QApplication.translate("dlgInputRestartYears", "The first year of restart run", None))
        self.leLastYear.setToolTip(QtWidgets.QApplication.translate("dlgInputRestartYears", "The last year of restart run", None))
        self.label_2.setText(QtWidgets.QApplication.translate("dlgInputRestartYears", "First Year:", None))
        self.label_3.setText(QtWidgets.QApplication.translate("dlgInputRestartYears", "Last Year:", None))
        self.label.setText(QtWidgets.QApplication.translate("dlgInputRestartYears", "End Year", None))
        self.label_4.setText(QtWidgets.QApplication.translate("dlgInputRestartYears", "Base Year", None))

