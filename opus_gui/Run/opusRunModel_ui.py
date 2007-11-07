# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusRunModel.ui'
#
# Created: Wed Nov  7 00:34:15 2007
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

        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox)
        self.hboxlayout.setObjectName("hboxlayout")

        self.widget = QtGui.QWidget(self.groupBox)
        self.widget.setObjectName("widget")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.runProgressBar = QtGui.QProgressBar(self.widget)
        self.runProgressBar.setProperty("value",QtCore.QVariant(24))
        self.runProgressBar.setObjectName("runProgressBar")
        self.vboxlayout1.addWidget(self.runProgressBar)

        self.runStatusLabel = QtGui.QLabel(self.widget)
        self.runStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.runStatusLabel.setObjectName("runStatusLabel")
        self.vboxlayout1.addWidget(self.runStatusLabel)
        self.hboxlayout.addWidget(self.widget)

        self.widget_3 = QtGui.QWidget(self.groupBox)
        self.widget_3.setObjectName("widget_3")

        self.gridlayout = QtGui.QGridLayout(self.widget_3)
        self.gridlayout.setObjectName("gridlayout")

        self.pbnStartModel = QtGui.QPushButton(self.widget_3)
        self.pbnStartModel.setObjectName("pbnStartModel")
        self.gridlayout.addWidget(self.pbnStartModel,0,0,1,1)
        self.hboxlayout.addWidget(self.widget_3)
        self.vboxlayout.addWidget(self.groupBox)

        self.widget_2 = QtGui.QWidget(OpusRunModel)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")

        self.gridlayout1 = QtGui.QGridLayout(self.widget_2)
        self.gridlayout1.setContentsMargins(-1,0,-1,0)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(251,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,0,1,1)

        self.pbnCancel = QtGui.QPushButton(self.widget_2)
        self.pbnCancel.setObjectName("pbnCancel")
        self.gridlayout1.addWidget(self.pbnCancel,0,1,1,1)
        self.vboxlayout.addWidget(self.widget_2)

        self.retranslateUi(OpusRunModel)
        QtCore.QMetaObject.connectSlotsByName(OpusRunModel)

    def retranslateUi(self, OpusRunModel):
        OpusRunModel.setWindowTitle(QtGui.QApplication.translate("OpusRunModel", "OpusGui - Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("OpusRunModel", "Current Model", None, QtGui.QApplication.UnicodeUTF8))
        self.runStatusLabel.setText(QtGui.QApplication.translate("OpusRunModel", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnStartModel.setText(QtGui.QApplication.translate("OpusRunModel", "Start Model", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnCancel.setText(QtGui.QApplication.translate("OpusRunModel", "Close", None, QtGui.QApplication.UnicodeUTF8))

