# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configurescript.ui'
#
# Created: Mon Jan 21 20:25:01 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ConfigureScriptGui(object):
    def setupUi(self, ConfigureScriptGui):
        ConfigureScriptGui.setObjectName("ConfigureScriptGui")
        ConfigureScriptGui.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(ConfigureScriptGui.minimumSizeHint()))

        self.buttonBox = QtGui.QDialogButtonBox(ConfigureScriptGui)
        self.buttonBox.setGeometry(QtCore.QRect(30,240,341,32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(ConfigureScriptGui)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),ConfigureScriptGui.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),ConfigureScriptGui.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigureScriptGui)

    def retranslateUi(self, ConfigureScriptGui):
        ConfigureScriptGui.setWindowTitle(QtGui.QApplication.translate("ConfigureScriptGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

