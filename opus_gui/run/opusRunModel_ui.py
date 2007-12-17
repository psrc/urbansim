# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusRunModel.ui'
#
# Created: Fri Nov 23 10:33:41 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_OpusRunModel(object):
    def setupUi(self, OpusRunModel):
        OpusRunModel.setObjectName("OpusRunModel")
        OpusRunModel.resize(QtCore.QSize(QtCore.QRect(0,0,877,674).size()).expandedTo(OpusRunModel.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OpusRunModel.sizePolicy().hasHeightForWidth())
        OpusRunModel.setSizePolicy(sizePolicy)

        self.vboxlayout = QtGui.QVBoxLayout(OpusRunModel)
        self.vboxlayout.setObjectName("vboxlayout")

        self.modelFrame = QtGui.QWidget(OpusRunModel)
        self.modelFrame.setObjectName("modelFrame")
        self.vboxlayout.addWidget(self.modelFrame)

        self.modelClose = QtGui.QWidget(OpusRunModel)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modelClose.sizePolicy().hasHeightForWidth())
        self.modelClose.setSizePolicy(sizePolicy)
        self.modelClose.setObjectName("modelClose")

        self.hboxlayout = QtGui.QHBoxLayout(self.modelClose)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(251,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pbnCancel = QtGui.QPushButton(self.modelClose)
        self.pbnCancel.setObjectName("pbnCancel")
        self.hboxlayout.addWidget(self.pbnCancel)
        self.vboxlayout.addWidget(self.modelClose)

        self.retranslateUi(OpusRunModel)
        QtCore.QMetaObject.connectSlotsByName(OpusRunModel)

    def retranslateUi(self, OpusRunModel):
        OpusRunModel.setWindowTitle(QtGui.QApplication.translate("OpusRunModel", "OpusGui - Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnCancel.setText(QtGui.QApplication.translate("OpusRunModel", "Close", None, QtGui.QApplication.UnicodeUTF8))

