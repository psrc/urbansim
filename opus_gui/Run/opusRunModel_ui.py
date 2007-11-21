# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusRunModel.ui'
#
# Created: Tue Nov 20 21:07:12 2007
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

        self.hboxlayout = QtGui.QHBoxLayout(self.widget_2)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(251,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pbnCancel = QtGui.QPushButton(self.widget_2)
        self.pbnCancel.setObjectName("pbnCancel")
        self.hboxlayout.addWidget(self.pbnCancel)
        self.vboxlayout.addWidget(self.widget_2)

        self.retranslateUi(OpusRunModel)
        QtCore.QMetaObject.connectSlotsByName(OpusRunModel)

    def retranslateUi(self, OpusRunModel):
        OpusRunModel.setWindowTitle(QtGui.QApplication.translate("OpusRunModel", "OpusGui - Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("OpusRunModel", "Models available to run...", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnCancel.setText(QtGui.QApplication.translate("OpusRunModel", "Close", None, QtGui.QApplication.UnicodeUTF8))

