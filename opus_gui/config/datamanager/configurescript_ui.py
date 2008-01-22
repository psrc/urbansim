# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configurescript.ui'
#
# Created: Mon Jan 21 21:29:03 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ConfigureScriptGui(object):
    def setupUi(self, ConfigureScriptGui):
        ConfigureScriptGui.setObjectName("ConfigureScriptGui")
        ConfigureScriptGui.resize(QtCore.QSize(QtCore.QRect(0,0,412,312).size()).expandedTo(ConfigureScriptGui.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ConfigureScriptGui)
        self.vboxlayout.setObjectName("vboxlayout")

        self.variableBox = QtGui.QGroupBox(ConfigureScriptGui)
        self.variableBox.setObjectName("variableBox")
        self.vboxlayout.addWidget(self.variableBox)

        self.widget = QtGui.QWidget(ConfigureScriptGui)
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

        self.retranslateUi(ConfigureScriptGui)
        QtCore.QMetaObject.connectSlotsByName(ConfigureScriptGui)

    def retranslateUi(self, ConfigureScriptGui):
        ConfigureScriptGui.setWindowTitle(QtGui.QApplication.translate("ConfigureScriptGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.variableBox.setTitle(QtGui.QApplication.translate("ConfigureScriptGui", "Script Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.createConfig.setText(QtGui.QApplication.translate("ConfigureScriptGui", "Create Config", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelConfig.setText(QtGui.QApplication.translate("ConfigureScriptGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

