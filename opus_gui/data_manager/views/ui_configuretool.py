# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuretool.ui'
#
# Created: Thu Nov 06 11:36:23 2008
#      by: PyQt5 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_ConfigureToolGui(object):
    def setupUi(self, ConfigureToolGui):
        ConfigureToolGui.setObjectName("ConfigureToolGui")
        ConfigureToolGui.resize(QtCore.QSize(QtCore.QRect(0,0,412,312).size()).expandedTo(ConfigureToolGui.minimumSizeHint()))

        self.vboxlayout = QtWidgets.QVBoxLayout(ConfigureToolGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.comboBox = QtWidgets.QComboBox(ConfigureToolGui)
        self.comboBox.setObjectName("comboBox")
        self.vboxlayout.addWidget(self.comboBox)

        self.variableBox = QtWidgets.QGroupBox(ConfigureToolGui)
        self.variableBox.setObjectName("variableBox")
        self.vboxlayout.addWidget(self.variableBox)

        self.widget = QtWidgets.QWidget(ConfigureToolGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.gridlayout = QtWidgets.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtWidgets.QSpacerItem(40,20,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,0,1,1)

        self.createConfig = QtWidgets.QPushButton(self.widget)
        self.createConfig.setObjectName("createConfig")
        self.gridlayout.addWidget(self.createConfig,0,1,1,1)

        self.cancelConfig = QtWidgets.QPushButton(self.widget)
        self.cancelConfig.setObjectName("cancelConfig")
        self.gridlayout.addWidget(self.cancelConfig,0,2,1,1)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(ConfigureToolGui)
        QtCore.QMetaObject.connectSlotsByName(ConfigureToolGui)

    def retranslateUi(self, ConfigureToolGui):
        ConfigureToolGui.setWindowTitle(QtWidgets.QApplication.translate("ConfigureToolGui", "Dialog", None, QtWidgets.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtWidgets.QApplication.translate("ConfigureToolGui", "Select Tool", None, QtWidgets.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtWidgets.QApplication.translate("ConfigureToolGui", "Tool Variables", None, QtWidgets.QApplication.UnicodeUTF8))
        self.createConfig.setText(QtWidgets.QApplication.translate("ConfigureToolGui", "Add Tool", None, QtWidgets.QApplication.UnicodeUTF8))
        self.cancelConfig.setText(QtWidgets.QApplication.translate("ConfigureToolGui", "Cancel", None, QtWidgets.QApplication.UnicodeUTF8))

