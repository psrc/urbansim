# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input_restart_years_dialog.ui'
#
# Created: Sat May  7 17:20:47 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgInputRestartYears(object):
    def setupUi(self, dlgInputRestartYears):
        dlgInputRestartYears.setObjectName("dlgInputRestartYears")
        dlgInputRestartYears.resize(413, 140)
        self.buttonBox = QtGui.QDialogButtonBox(dlgInputRestartYears)
        self.buttonBox.setGeometry(QtCore.QRect(60, 97, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.leFirstYear = QtGui.QLineEdit(dlgInputRestartYears)
        self.leFirstYear.setGeometry(QtCore.QRect(213, 52, 81, 25))
        self.leFirstYear.setObjectName("leFirstYear")
        self.leLastYear = QtGui.QLineEdit(dlgInputRestartYears)
        self.leLastYear.setGeometry(QtCore.QRect(307, 52, 81, 25))
        self.leLastYear.setObjectName("leLastYear")
        self.label_2 = QtGui.QLabel(dlgInputRestartYears)
        self.label_2.setGeometry(QtCore.QRect(213, 29, 63, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(dlgInputRestartYears)
        self.label_3.setGeometry(QtCore.QRect(307, 29, 62, 17))
        self.label_3.setObjectName("label_3")
        self.lblEndYear = QtGui.QLabel(dlgInputRestartYears)
        self.lblEndYear.setGeometry(QtCore.QRect(118, 53, 81, 25))
        self.lblEndYear.setText("")
        self.lblEndYear.setObjectName("lblEndYear")
        self.label = QtGui.QLabel(dlgInputRestartYears)
        self.label.setGeometry(QtCore.QRect(118, 29, 57, 17))
        self.label.setObjectName("label")
        self.label_4 = QtGui.QLabel(dlgInputRestartYears)
        self.label_4.setGeometry(QtCore.QRect(25, 29, 65, 17))
        self.label_4.setObjectName("label_4")
        self.lblBaseYear = QtGui.QLabel(dlgInputRestartYears)
        self.lblBaseYear.setGeometry(QtCore.QRect(25, 53, 81, 25))
        self.lblBaseYear.setText("")
        self.lblBaseYear.setObjectName("lblBaseYear")

        self.retranslateUi(dlgInputRestartYears)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dlgInputRestartYears.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dlgInputRestartYears.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgInputRestartYears)

    def retranslateUi(self, dlgInputRestartYears):
        dlgInputRestartYears.setWindowTitle(QtGui.QApplication.translate("dlgInputRestartYears", "The First and Last Year of Restart Run", None, QtGui.QApplication.UnicodeUTF8))
        self.leFirstYear.setToolTip(QtGui.QApplication.translate("dlgInputRestartYears", "The first year of restart run", None, QtGui.QApplication.UnicodeUTF8))
        self.leLastYear.setToolTip(QtGui.QApplication.translate("dlgInputRestartYears", "The last year of restart run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dlgInputRestartYears", "First Year:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("dlgInputRestartYears", "Last Year:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgInputRestartYears", "End Year", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("dlgInputRestartYears", "Base Year", None, QtGui.QApplication.UnicodeUTF8))

