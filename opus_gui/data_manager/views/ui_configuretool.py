# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuretool.ui'
#
# Created: Thu Nov 06 11:36:23 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ConfigureToolGui(object):
    def setupUi(self, ConfigureToolGui):
        ConfigureToolGui.setObjectName("ConfigureToolGui")
        ConfigureToolGui.resize(QtCore.QSize(QtCore.QRect(0,0,412,312).size()).expandedTo(ConfigureToolGui.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ConfigureToolGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.comboBox = QtGui.QComboBox(ConfigureToolGui)
        self.comboBox.setObjectName("comboBox")
        self.vboxlayout.addWidget(self.comboBox)

        self.variableBox = QtGui.QGroupBox(ConfigureToolGui)
        self.variableBox.setObjectName("variableBox")
        self.vboxlayout.addWidget(self.variableBox)

        self.widget = QtGui.QWidget(ConfigureToolGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.gridlayout = QtGui.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,0,1,1)

        self.createConfig = QtGui.QPushButton(self.widget)
        self.createConfig.setObjectName("createConfig")
        self.gridlayout.addWidget(self.createConfig,0,1,1,1)

        self.cancelConfig = QtGui.QPushButton(self.widget)
        self.cancelConfig.setObjectName("cancelConfig")
        self.gridlayout.addWidget(self.cancelConfig,0,2,1,1)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(ConfigureToolGui)
        QtCore.QMetaObject.connectSlotsByName(ConfigureToolGui)

    def retranslateUi(self, ConfigureToolGui):
        ConfigureToolGui.setWindowTitle(QtGui.QApplication.translate("ConfigureToolGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("ConfigureToolGui", "Select Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("ConfigureToolGui", "Tool Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.createConfig.setText(QtGui.QApplication.translate("ConfigureToolGui", "Add Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelConfig.setText(QtGui.QApplication.translate("ConfigureToolGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

