# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/travis/Documents/workspace/opus/opus_gui/run/estimation_gui_element.ui'
#
# Created: Thu Sep 25 11:57:22 2008
#      by: PyQt5 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_EstimationGuiElement(object):
    def setupUi(self, EstimationGuiElement):
        EstimationGuiElement.setObjectName("EstimationGuiElement")
        EstimationGuiElement.resize(709, 546)
        self.widgetLayout = QtWidgets.QGridLayout(EstimationGuiElement)
        self.widgetLayout.setObjectName("widgetLayout")
        self.pbnStartModel = QtWidgets.QPushButton(EstimationGuiElement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbnStartModel.sizePolicy().hasHeightForWidth())
        self.pbnStartModel.setSizePolicy(sizePolicy)
        self.pbnStartModel.setObjectName("pbnStartModel")
        self.widgetLayout.addWidget(self.pbnStartModel, 0, 0, 1, 1)
        self.runProgressBar = QtWidgets.QProgressBar(EstimationGuiElement)
        self.runProgressBar.setProperty("value", QtCore.QVariant(24))
        self.runProgressBar.setObjectName("runProgressBar")
        self.widgetLayout.addWidget(self.runProgressBar, 0, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.widgetLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.runStatusLabel = QtWidgets.QLabel(EstimationGuiElement)
        self.runStatusLabel.setObjectName("runStatusLabel")
        self.widgetLayout.addWidget(self.runStatusLabel, 1, 2, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(EstimationGuiElement)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setGeometry(QtCore.QRect(0, 0, 679, 431))
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setContentsMargins(0, 5, 0, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.logText = QtWidgets.QTextEdit(self.tab)
        self.logText.setLineWidth(0)
        self.logText.setReadOnly(True)
        self.logText.setObjectName("logText")
        self.gridLayout.addWidget(self.logText, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.widgetLayout.addWidget(self.tabWidget, 2, 0, 1, 3)

        self.retranslateUi(EstimationGuiElement)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(EstimationGuiElement)

    def retranslateUi(self, EstimationGuiElement):
        EstimationGuiElement.setWindowTitle(QtWidgets.QApplication.translate("EstimationGuiElement", "Form", None, QtWidgets.QApplication.UnicodeUTF8))
        self.pbnStartModel.setText(QtWidgets.QApplication.translate("EstimationGuiElement", "Start Estimation...", None, QtWidgets.QApplication.UnicodeUTF8))
        self.runStatusLabel.setText(QtWidgets.QApplication.translate("EstimationGuiElement", "Press Start to run the estimation...", None, QtWidgets.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtWidgets.QApplication.translate("EstimationGuiElement", "Estimation result log", None, QtWidgets.QApplication.UnicodeUTF8))

