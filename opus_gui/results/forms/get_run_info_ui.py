# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_run_info.ui'
#
# Created: Thu Jun 19 16:37:30 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgGetRunInfo(object):
    def setupUi(self, dlgGetRunInfo):
        dlgGetRunInfo.setObjectName("dlgGetRunInfo")
        dlgGetRunInfo.resize(629, 262)
        self.btnDone = QtGui.QPushButton(dlgGetRunInfo)
        self.btnDone.setGeometry(QtCore.QRect(530, 220, 71, 32))
        self.btnDone.setObjectName("btnDone")
        self.widget = QtGui.QWidget(dlgGetRunInfo)
        self.widget.setGeometry(QtCore.QRect(10, 25, 591, 191))
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.lblScenario_name = QtGui.QLabel(self.widget)
        self.lblScenario_name.setTextFormat(QtCore.Qt.AutoText)
        self.lblScenario_name.setObjectName("lblScenario_name")
        self.gridLayout.addWidget(self.lblScenario_name, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lblRun_name = QtGui.QLabel(self.widget)
        self.lblRun_name.setWordWrap(True)
        self.lblRun_name.setObjectName("lblRun_name")
        self.gridLayout.addWidget(self.lblRun_name, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lblYears_run = QtGui.QLabel(self.widget)
        self.lblYears_run.setObjectName("lblYears_run")
        self.gridLayout.addWidget(self.lblYears_run, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.lblCache_directory = QtGui.QLabel(self.widget)
        self.lblCache_directory.setWordWrap(True)
        self.lblCache_directory.setObjectName("lblCache_directory")
        self.gridLayout.addWidget(self.lblCache_directory, 4, 0, 1, 2)

        self.retranslateUi(dlgGetRunInfo)
        QtCore.QMetaObject.connectSlotsByName(dlgGetRunInfo)

    def retranslateUi(self, dlgGetRunInfo):
        dlgGetRunInfo.setWindowTitle(QtGui.QApplication.translate("dlgGetRunInfo", "Details for simulation run", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDone.setText(QtGui.QApplication.translate("dlgGetRunInfo", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("dlgGetRunInfo", "Scenario:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblScenario_name.setText(QtGui.QApplication.translate("dlgGetRunInfo", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgGetRunInfo", "Run name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblRun_name.setText(QtGui.QApplication.translate("dlgGetRunInfo", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dlgGetRunInfo", "Years run:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblYears_run.setText(QtGui.QApplication.translate("dlgGetRunInfo", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("dlgGetRunInfo", "Cache directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCache_directory.setText(QtGui.QApplication.translate("dlgGetRunInfo", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

