# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusAbout.ui'
#
# Created: Tue Jan 08 13:58:24 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_UrbansimAbout(object):
    def setupUi(self, UrbansimAbout):
        UrbansimAbout.setObjectName("UrbansimAbout")
        UrbansimAbout.resize(QtCore.QSize(QtCore.QRect(0,0,534,344).size()).expandedTo(UrbansimAbout.minimumSizeHint()))
        UrbansimAbout.setWindowIcon(QtGui.QIcon(":/Images/Images/exclamation.png"))
        UrbansimAbout.setSizeGripEnabled(True)

        self.urbansimLabel = QtGui.QLabel(UrbansimAbout)
        self.urbansimLabel.setGeometry(QtCore.QRect(220,0,85,21))

        font = QtGui.QFont()
        font.setPointSize(18)
        font.setWeight(75)
        font.setBold(True)
        self.urbansimLabel.setFont(font)
        self.urbansimLabel.setTextFormat(QtCore.Qt.RichText)
        self.urbansimLabel.setScaledContents(True)
        self.urbansimLabel.setObjectName("urbansimLabel")

        self.webPushButton = QtGui.QPushButton(UrbansimAbout)
        self.webPushButton.setGeometry(QtCore.QRect(130,210,281,24))
        self.webPushButton.setObjectName("webPushButton")

        self.docPushButton = QtGui.QPushButton(UrbansimAbout)
        self.docPushButton.setGeometry(QtCore.QRect(130,240,281,24))
        self.docPushButton.setObjectName("docPushButton")

        self.aboutTextEdit = QtGui.QTextEdit(UrbansimAbout)
        self.aboutTextEdit.setGeometry(QtCore.QRect(10,20,511,181))
        self.aboutTextEdit.setObjectName("aboutTextEdit")

        self.licensePushButton = QtGui.QPushButton(UrbansimAbout)
        self.licensePushButton.setGeometry(QtCore.QRect(130,270,281,24))
        self.licensePushButton.setObjectName("licensePushButton")

        self.layoutWidget = QtGui.QWidget(UrbansimAbout)
        self.layoutWidget.setGeometry(QtCore.QRect(10,300,511,26))
        self.layoutWidget.setObjectName("layoutWidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(20,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.buttonCancel = QtGui.QPushButton(self.layoutWidget)
        self.buttonCancel.setAutoDefault(True)
        self.buttonCancel.setObjectName("buttonCancel")
        self.hboxlayout.addWidget(self.buttonCancel)

        self.retranslateUi(UrbansimAbout)
        QtCore.QMetaObject.connectSlotsByName(UrbansimAbout)

    def retranslateUi(self, UrbansimAbout):
        UrbansimAbout.setWindowTitle(QtGui.QApplication.translate("UrbansimAbout", "About Urbansim", None, QtGui.QApplication.UnicodeUTF8))
        self.urbansimLabel.setText(QtGui.QApplication.translate("UrbansimAbout", "UrbanSim", None, QtGui.QApplication.UnicodeUTF8))
        self.webPushButton.setText(QtGui.QApplication.translate("UrbansimAbout", "Web Site", None, QtGui.QApplication.UnicodeUTF8))
        self.docPushButton.setText(QtGui.QApplication.translate("UrbansimAbout", "Documentation", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutTextEdit.setHtml(QtGui.QApplication.translate("UrbansimAbout", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Helvetica\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">UrbanSim is a software-based simulation model for integrated planning and analysis of urban development, incorporating the interactions between land use, transportation, and public policy. It is intended for use by Metropolitan Planning Organizations and others needing to interface existing travel models with new land use forecasting and analysis capabilities.  UrbanSim is the centerpiece of the research activities of the Center for Urban Simulation and Policy Analysis, located at the Point 5 Laboratory, on the Ave a few blocks from the University of Washington campus. The UrbanSim software, including full source code, is available for download via this website. It is licensed under the GNU General Public License, which means it is free, open source, and any derived works are also covered under the license. The intent of this licensing approach is to avoid proprietary obstacles and costs, and to facilitate collaboration between researchers and practitioners in improving land use and transportation planning and policy.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.licensePushButton.setText(QtGui.QApplication.translate("UrbansimAbout", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("UrbansimAbout", "Ok", None, QtGui.QApplication.UnicodeUTF8))

import opusMain_rc
