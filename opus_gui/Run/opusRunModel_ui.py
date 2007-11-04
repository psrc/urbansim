# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusRunModel.ui'
#
# Created: Sat Nov  3 13:47:26 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_OpusRunModel(object):
    def setupUi(self, OpusRunModel):
        OpusRunModel.setObjectName("OpusRunModel")
        OpusRunModel.resize(QtCore.QSize(QtCore.QRect(0,0,400,125).size()).expandedTo(OpusRunModel.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(OpusRunModel)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.widget = QtGui.QWidget(OpusRunModel)
        self.widget.setObjectName("widget")

        self.hboxlayout = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setObjectName("hboxlayout")

        self.model_text = QtGui.QLabel(self.widget)
        self.model_text.setObjectName("model_text")
        self.hboxlayout.addWidget(self.model_text)
        self.vboxlayout.addWidget(self.widget)

        self.widget_2 = QtGui.QWidget(OpusRunModel)
        self.widget_2.setObjectName("widget_2")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.widget_2)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.pbnCancel = QtGui.QPushButton(self.widget_2)
        self.pbnCancel.setObjectName("pbnCancel")
        self.hboxlayout1.addWidget(self.pbnCancel)

        self.pbnStartModel = QtGui.QPushButton(self.widget_2)
        self.pbnStartModel.setObjectName("pbnStartModel")
        self.hboxlayout1.addWidget(self.pbnStartModel)
        self.vboxlayout.addWidget(self.widget_2)

        self.retranslateUi(OpusRunModel)
        QtCore.QMetaObject.connectSlotsByName(OpusRunModel)

    def retranslateUi(self, OpusRunModel):
        OpusRunModel.setWindowTitle(QtGui.QApplication.translate("OpusRunModel", "OpusGui - Run Model", None, QtGui.QApplication.UnicodeUTF8))
        self.model_text.setText(QtGui.QApplication.translate("OpusRunModel", "Starting to run the model...", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnCancel.setText(QtGui.QApplication.translate("OpusRunModel", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnStartModel.setText(QtGui.QApplication.translate("OpusRunModel", "Start Model", None, QtGui.QApplication.UnicodeUTF8))

