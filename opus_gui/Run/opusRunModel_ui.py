# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusRunModel.ui'
#
# Created: Mon Nov 19 15:13:04 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_OpusRunModel(object):
    def setupUi(self, OpusRunModel):
        OpusRunModel.setObjectName("OpusRunModel")
        OpusRunModel.resize(QtCore.QSize(QtCore.QRect(0,0,718,147).size()).expandedTo(OpusRunModel.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(OpusRunModel)
        self.vboxlayout.setObjectName("vboxlayout")

        self.groupBox = QtGui.QGroupBox(OpusRunModel)
        self.groupBox.setObjectName("groupBox")
        self.vboxlayout.addWidget(self.groupBox)

        self.widget_2 = QtGui.QWidget(OpusRunModel)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")

        self.gridlayout = QtGui.QGridLayout(self.widget_2)
        self.gridlayout.setContentsMargins(-1,0,-1,0)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(251,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,0,1,1)

        self.pbnCancel = QtGui.QPushButton(self.widget_2)
        self.pbnCancel.setObjectName("pbnCancel")
        self.gridlayout.addWidget(self.pbnCancel,0,1,1,1)
        self.vboxlayout.addWidget(self.widget_2)

        self.retranslateUi(OpusRunModel)
        QtCore.QMetaObject.connectSlotsByName(OpusRunModel)

    def retranslateUi(self, OpusRunModel):
        OpusRunModel.setWindowTitle(QtGui.QApplication.translate("OpusRunModel", "OpusGui - Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("OpusRunModel", "Models available to run...", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnCancel.setText(QtGui.QApplication.translate("OpusRunModel", "Close", None, QtGui.QApplication.UnicodeUTF8))

