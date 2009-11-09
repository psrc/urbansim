# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/opus_trunk/opus_gui/main/views/opusabout.ui'
#
# Created: Sun May 10 00:57:44 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_UrbansimAbout(object):
    def setupUi(self, UrbansimAbout):
        UrbansimAbout.setObjectName("UrbansimAbout")
        UrbansimAbout.resize(581, 474)
        UrbansimAbout.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(UrbansimAbout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.aboutTextEdit = QtGui.QTextEdit(UrbansimAbout)
        self.aboutTextEdit.setUndoRedoEnabled(True)
        self.aboutTextEdit.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.aboutTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.aboutTextEdit.setObjectName("aboutTextEdit")
        self.verticalLayout.addWidget(self.aboutTextEdit)
        self.webPushButton = QtGui.QPushButton(UrbansimAbout)
        self.webPushButton.setObjectName("webPushButton")
        self.verticalLayout.addWidget(self.webPushButton)
        self.docPushButton = QtGui.QPushButton(UrbansimAbout)
        self.docPushButton.setObjectName("docPushButton")
        self.verticalLayout.addWidget(self.docPushButton)
        self.licensePushButton = QtGui.QPushButton(UrbansimAbout)
        self.licensePushButton.setObjectName("licensePushButton")
        self.verticalLayout.addWidget(self.licensePushButton)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.buttonCancel = QtGui.QPushButton(UrbansimAbout)
        self.buttonCancel.setAutoDefault(True)
        self.buttonCancel.setObjectName("buttonCancel")
        self.hboxlayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.hboxlayout)

        self.retranslateUi(UrbansimAbout)
        QtCore.QMetaObject.connectSlotsByName(UrbansimAbout)

    def retranslateUi(self, UrbansimAbout):
        UrbansimAbout.setWindowTitle(QtGui.QApplication.translate("UrbansimAbout", "About Urbansim", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutTextEdit.setHtml(QtGui.QApplication.translate("UrbansimAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:10px; margin-bottom:10px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; vertical-align:middle;\"><img src=\":/Images/Images/logo64px.png\" style=\"vertical-align: middle;\" />  <span style=\" font-size:18pt; font-weight:600;\">Urbansim</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">UrbanSim is a software-based simulation model for integrated planning and analysis of urban development, incorporating the interactions between land use, transportation, and public policy. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">It is intended for use by Metropolitan Planning Organizations and others needing to interface existing travel models with new land use forecasting and analysis capabilities. UrbanSim is the centerpiece of the research activities of the Center for Urban Simulation and Policy Analysis, located at the Point 5 Laboratory, on the Ave a few blocks from the University of Washington campus. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The UrbanSim software, including full source code, is available for download via the webside below. It is licensed under the GNU General Public License, which means it is free, open source, and any derived works are also covered under the license. The intent of this licensing approach is to avoid proprietary obstacles and costs, and to facilitate collaboration between researchers and practitioners in improving land use and transportation planning and policy.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.webPushButton.setText(QtGui.QApplication.translate("UrbansimAbout", "Web Site", None, QtGui.QApplication.UnicodeUTF8))
        self.docPushButton.setText(QtGui.QApplication.translate("UrbansimAbout", "Documentation", None, QtGui.QApplication.UnicodeUTF8))
        self.licensePushButton.setText(QtGui.QApplication.translate("UrbansimAbout", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("UrbansimAbout", "Ok", None, QtGui.QApplication.UnicodeUTF8))

import opusmain_rc
