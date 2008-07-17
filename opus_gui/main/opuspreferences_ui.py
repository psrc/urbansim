# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opuspreferences.ui'
#
# Created: Wed Jul 16 11:57:44 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName("PreferencesDialog")
        PreferencesDialog.resize(390,155)
        self.fontGroupBox = QtGui.QGroupBox(PreferencesDialog)
        self.fontGroupBox.setGeometry(QtCore.QRect(10,20,361,71))
        self.fontGroupBox.setObjectName("fontGroupBox")
        self.fontSizeAdjustLabel = QtGui.QLabel(self.fontGroupBox)
        self.fontSizeAdjustLabel.setGeometry(QtCore.QRect(20,20,111,31))
        self.fontSizeAdjustLabel.setObjectName("fontSizeAdjustLabel")
        self.fontSizeAdjustSlider = QtGui.QSlider(self.fontGroupBox)
        self.fontSizeAdjustSlider.setGeometry(QtCore.QRect(150,30,191,21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontSizeAdjustSlider.sizePolicy().hasHeightForWidth())
        self.fontSizeAdjustSlider.setSizePolicy(sizePolicy)
        self.fontSizeAdjustSlider.setMinimum(-5)
        self.fontSizeAdjustSlider.setMaximum(10)
        self.fontSizeAdjustSlider.setOrientation(QtCore.Qt.Horizontal)
        self.fontSizeAdjustSlider.setObjectName("fontSizeAdjustSlider")
        self.cancelButton = QtGui.QPushButton(PreferencesDialog)
        self.cancelButton.setGeometry(QtCore.QRect(290,110,75,23))
        self.cancelButton.setObjectName("cancelButton")
        self.okButton = QtGui.QPushButton(PreferencesDialog)
        self.okButton.setGeometry(QtCore.QRect(130,110,75,23))
        self.okButton.setAutoDefault(True)
        self.okButton.setObjectName("okButton")
        self.applyButton = QtGui.QPushButton(PreferencesDialog)
        self.applyButton.setGeometry(QtCore.QRect(210,110,75,23))
        self.applyButton.setAutoDefault(True)
        self.applyButton.setObjectName("applyButton")

        self.retranslateUi(PreferencesDialog)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialog)

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QtGui.QApplication.translate("PreferencesDialog", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.fontGroupBox.setTitle(QtGui.QApplication.translate("PreferencesDialog", "Font Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.fontSizeAdjustLabel.setText(QtGui.QApplication.translate("PreferencesDialog", "Font Size Adjustment", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("PreferencesDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("PreferencesDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtGui.QApplication.translate("PreferencesDialog", "Apply", None, QtGui.QApplication.UnicodeUTF8))

