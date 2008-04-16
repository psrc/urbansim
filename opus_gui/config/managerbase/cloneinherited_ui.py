# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cloneinherited.ui'
#
# Created: Tue Apr  8 00:01:09 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CloneInheritedGui(object):
    def setupUi(self, CloneInheritedGui):
        CloneInheritedGui.setObjectName("CloneInheritedGui")
        CloneInheritedGui.resize(QtCore.QSize(QtCore.QRect(0,0,658,626).size()).expandedTo(CloneInheritedGui.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(CloneInheritedGui)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(CloneInheritedGui)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.xmlBox = QtGui.QGroupBox(CloneInheritedGui)
        self.xmlBox.setObjectName("xmlBox")
        self.gridlayout.addWidget(self.xmlBox,1,0,1,1)

        self.widget = QtGui.QWidget(CloneInheritedGui)
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

        self.retranslateUi(CloneInheritedGui)
        QtCore.QMetaObject.connectSlotsByName(CloneInheritedGui)

    def retranslateUi(self, CloneInheritedGui):
        CloneInheritedGui.setWindowTitle(QtGui.QApplication.translate("CloneInheritedGui", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CloneInheritedGui", "Please Select Where To Drop Your Node", None, QtGui.QApplication.UnicodeUTF8))
        self.xmlBox.setTitle(QtGui.QApplication.translate("CloneInheritedGui", "Personal XML", None, QtGui.QApplication.UnicodeUTF8))
        self.createXML.setText(QtGui.QApplication.translate("CloneInheritedGui", "Drop In XML", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelXML.setText(QtGui.QApplication.translate("CloneInheritedGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

