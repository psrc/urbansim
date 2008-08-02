# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_run_info.ui'
#
# Created: Sat Aug  2 11:47:20 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgGetRunInfo(object):
    def setupUi(self, dlgGetRunInfo):
        dlgGetRunInfo.setObjectName("dlgGetRunInfo")
        dlgGetRunInfo.resize(614, 204)
        self.btnDone = QtGui.QPushButton(dlgGetRunInfo)
        self.btnDone.setGeometry(QtCore.QRect(530, 170, 71, 32))
        self.btnDone.setObjectName("btnDone")
        self.layoutWidget = QtGui.QWidget(dlgGetRunInfo)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 591, 154))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.lblScenario_name = QtGui.QLabel(self.layoutWidget)
        self.lblScenario_name.setTextFormat(QtCore.Qt.AutoText)
        self.lblScenario_name.setObjectName("lblScenario_name")
        self.gridLayout.addWidget(self.lblScenario_name, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lblRun_name = QtGui.QLabel(self.layoutWidget)
        self.lblRun_name.setWordWrap(True)
        self.lblRun_name.setObjectName("lblRun_name")
        self.gridLayout.addWidget(self.lblRun_name, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.lblYears_run = QtGui.QLabel(self.layoutWidget)
        self.lblYears_run.setObjectName("lblYears_run")
        self.gridLayout.addWidget(self.lblYears_run, 3, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.lblCache_directory = QtGui.QLabel(self.layoutWidget)
        self.lblCache_directory.setWordWrap(True)
        self.lblCache_directory.setObjectName("lblCache_directory")
        self.gridLayout.addWidget(self.lblCache_directory, 5, 0, 1, 2)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.lblRunId = QtGui.QLabel(self.layoutWidget)
        self.lblRunId.setTextFormat(QtCore.Qt.AutoText)
        self.lblRunId.setObjectName("lblRunId")
        self.gridLayout.addWidget(self.lblRunId, 0, 1, 1, 1)

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
        self.label_5.setText(QtGui.QApplication.translate("dlgGetRunInfo", "Run id:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblRunId.setText(QtGui.QApplication.translate("dlgGetRunInfo", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

