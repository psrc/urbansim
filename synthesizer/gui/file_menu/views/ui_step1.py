# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'step1.ui'
#
# Created: Fri Nov 14 17:29:27 2008
#      by: PyQt5 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_wizardStep1Dialog(object):
    def setupUi(self, wizardStep1Dialog):
        wizardStep1Dialog.setObjectName("wizardStep1Dialog")
        wizardStep1Dialog.setWindowModality(QtCore.Qt.NonModal)
        wizardStep1Dialog.resize(1035,629)
        self.nextWizButton = QtWidgets.QPushButton(wizardStep1Dialog)
        self.nextWizButton.setGeometry(QtCore.QRect(800,580,91,31))
        self.nextWizButton.setObjectName("nextWizButton")
        self.cancelWizButton = QtWidgets.QPushButton(wizardStep1Dialog)
        self.cancelWizButton.setGeometry(QtCore.QRect(920,580,91,31))
        self.cancelWizButton.setObjectName("cancelWizButton")
        self.wizFrame = QtWidgets.QFrame(wizardStep1Dialog)
        self.wizFrame.setGeometry(QtCore.QRect(320,20,701,551))
        self.wizFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.wizFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.wizFrame.setObjectName("wizFrame")
        self.wizTreeView = QtWidgets.QTreeView(wizardStep1Dialog)
        self.wizTreeView.setGeometry(QtCore.QRect(10,330,301,241))
        self.wizTreeView.setObjectName("wizTreeView")
        self.newWizGroupBox = QtWidgets.QGroupBox(wizardStep1Dialog)
        self.newWizGroupBox.setGeometry(QtCore.QRect(10,10,301,311))
        self.newWizGroupBox.setObjectName("newWizGroupBox")
        self.nameLabel = QtWidgets.QLabel(self.newWizGroupBox)
        self.nameLabel.setGeometry(QtCore.QRect(10,30,46,14))
        self.nameLabel.setObjectName("nameLabel")
        self.nameLineEdit = QtWidgets.QLineEdit(self.newWizGroupBox)
        self.nameLineEdit.setGeometry(QtCore.QRect(10,50,261,20))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.namePromptLabel = QtWidgets.QLabel(self.newWizGroupBox)
        self.namePromptLabel.setGeometry(QtCore.QRect(20,70,261,16))
        self.namePromptLabel.setObjectName("namePromptLabel")
        self.locationLabel = QtWidgets.QLabel(self.newWizGroupBox)
        self.locationLabel.setGeometry(QtCore.QRect(10,90,46,14))
        self.locationLabel.setObjectName("locationLabel")
        self.locationLineEdit = QtWidgets.QLineEdit(self.newWizGroupBox)
        self.locationLineEdit.setGeometry(QtCore.QRect(10,110,241,20))
        self.locationLineEdit.setObjectName("locationLineEdit")
        self.locationPromptLabel = QtWidgets.QLabel(self.newWizGroupBox)
        self.locationPromptLabel.setGeometry(QtCore.QRect(20,130,261,16))
        self.locationPromptLabel.setObjectName("locationPromptLabel")
        self.locationBrowserButton = QtWidgets.QPushButton(self.newWizGroupBox)
        self.locationBrowserButton.setGeometry(QtCore.QRect(260,110,31,23))
        self.locationBrowserButton.setObjectName("locationBrowserButton")
        self.descriptionLabel = QtWidgets.QLabel(self.newWizGroupBox)
        self.descriptionLabel.setGeometry(QtCore.QRect(10,150,131,16))
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.descriptionTextEdit = QtWidgets.QTextEdit(self.newWizGroupBox)
        self.descriptionTextEdit.setGeometry(QtCore.QRect(10,170,281,131))
        self.descriptionTextEdit.setObjectName("descriptionTextEdit")

        self.retranslateUi(wizardStep1Dialog)
        QtCore.QMetaObject.connectSlotsByName(wizardStep1Dialog)

    def retranslateUi(self, wizardStep1Dialog):
        wizardStep1Dialog.setWindowTitle(QtWidgets.QApplication.translate("wizardStep1Dialog", "Project Wizard", None, QtWidgets.QApplication.UnicodeUTF8))
        self.nextWizButton.setText(QtWidgets.QApplication.translate("wizardStep1Dialog", "Next >>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.cancelWizButton.setText(QtWidgets.QApplication.translate("wizardStep1Dialog", "Cancel", None, QtWidgets.QApplication.UnicodeUTF8))
        self.newWizGroupBox.setTitle(QtWidgets.QApplication.translate("wizardStep1Dialog", "New Project", None, QtWidgets.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtWidgets.QApplication.translate("wizardStep1Dialog", "Name", None, QtWidgets.QApplication.UnicodeUTF8))
        self.namePromptLabel.setText(QtWidgets.QApplication.translate("wizardStep1Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; color:#0000ff;\">Enter name</span></p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.locationLabel.setText(QtWidgets.QApplication.translate("wizardStep1Dialog", "Location", None, QtWidgets.QApplication.UnicodeUTF8))
        self.locationPromptLabel.setText(QtWidgets.QApplication.translate("wizardStep1Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" color:#0000ff;\">Enter location</span></p></body></html>", None, QtWidgets.QApplication.UnicodeUTF8))
        self.locationBrowserButton.setText(QtWidgets.QApplication.translate("wizardStep1Dialog", "...", None, QtWidgets.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtWidgets.QApplication.translate("wizardStep1Dialog", "Description", None, QtWidgets.QApplication.UnicodeUTF8))

