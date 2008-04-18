# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clonenode.ui'
#
# Created: Thu Apr 17 20:11:27 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CloneNodeGui(object):
    def setupUi(self, CloneNodeGui):
        CloneNodeGui.setObjectName("CloneNodeGui")
        CloneNodeGui.resize(QtCore.QSize(QtCore.QRect(0,0,658,147).size()).expandedTo(CloneNodeGui.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(CloneNodeGui)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(CloneNodeGui)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.xmlBox = QtGui.QGroupBox(CloneNodeGui)
        self.xmlBox.setObjectName("xmlBox")

        self.hboxlayout = QtGui.QHBoxLayout(self.xmlBox)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_2 = QtGui.QLabel(self.xmlBox)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)

        self.newName = QtGui.QLineEdit(self.xmlBox)
        self.newName.setObjectName("newName")
        self.hboxlayout.addWidget(self.newName)
        self.gridlayout.addWidget(self.xmlBox,1,0,1,1)

        self.widget = QtGui.QWidget(CloneNodeGui)
        self.widget.setMaximumSize(QtCore.QSize(16777215,45))
        self.widget.setObjectName("widget")

        self.gridlayout1 = QtGui.QGridLayout(self.widget)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,0,1,1)

        self.createXML = QtGui.QPushButton(self.widget)
        self.createXML.setObjectName("createXML")
        self.gridlayout1.addWidget(self.createXML,0,1,1,1)

        self.cancelXML = QtGui.QPushButton(self.widget)
        self.cancelXML.setObjectName("cancelXML")
        self.gridlayout1.addWidget(self.cancelXML,0,2,1,1)
        self.gridlayout.addWidget(self.widget,2,0,1,1)

        self.retranslateUi(CloneNodeGui)
        QtCore.QMetaObject.connectSlotsByName(CloneNodeGui)

    def retranslateUi(self, CloneNodeGui):
        CloneNodeGui.setWindowTitle(QtGui.QApplication.translate("CloneNodeGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CloneNodeGui", "Please select a new name for your copied node", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CloneNodeGui", "XML Node Name", None, QtGui.QApplication.UnicodeUTF8))
        self.createXML.setText(QtGui.QApplication.translate("CloneNodeGui", "Copy Into XML", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelXML.setText(QtGui.QApplication.translate("CloneNodeGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

