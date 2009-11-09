# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opuspreferences.ui'
#
# Created: Wed Oct 01 08:21:12 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName("PreferencesDialog")
        PreferencesDialog.resize(QtCore.QSize(QtCore.QRect(0,0,438,215).size()).expandedTo(PreferencesDialog.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PreferencesDialog.sizePolicy().hasHeightForWidth())
        PreferencesDialog.setSizePolicy(sizePolicy)

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesDialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.fontGroupBox = QtGui.QGroupBox(PreferencesDialog)
        self.fontGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.fontGroupBox.setObjectName("fontGroupBox")

        self.gridlayout = QtGui.QGridLayout(self.fontGroupBox)
        self.gridlayout.setObjectName("gridlayout")

        self.menuFontSizeLabel = QtGui.QLabel(self.fontGroupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuFontSizeLabel.sizePolicy().hasHeightForWidth())
        self.menuFontSizeLabel.setSizePolicy(sizePolicy)
        self.menuFontSizeLabel.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.menuFontSizeLabel.setObjectName("menuFontSizeLabel")
        self.gridlayout.addWidget(self.menuFontSizeLabel,0,0,1,1)

        self.menuFontSizeSpinBox = QtGui.QSpinBox(self.fontGroupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuFontSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.menuFontSizeSpinBox.setSizePolicy(sizePolicy)
        self.menuFontSizeSpinBox.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.menuFontSizeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.menuFontSizeSpinBox.setObjectName("menuFontSizeSpinBox")
        self.gridlayout.addWidget(self.menuFontSizeSpinBox,0,1,1,1)

        self.mainTabsFontSizeLabel = QtGui.QLabel(self.fontGroupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainTabsFontSizeLabel.sizePolicy().hasHeightForWidth())
        self.mainTabsFontSizeLabel.setSizePolicy(sizePolicy)
        self.mainTabsFontSizeLabel.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.mainTabsFontSizeLabel.setObjectName("mainTabsFontSizeLabel")
        self.gridlayout.addWidget(self.mainTabsFontSizeLabel,1,0,1,1)

        self.mainTabsFontSizeSpinBox = QtGui.QSpinBox(self.fontGroupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainTabsFontSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.mainTabsFontSizeSpinBox.setSizePolicy(sizePolicy)
        self.mainTabsFontSizeSpinBox.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.mainTabsFontSizeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mainTabsFontSizeSpinBox.setObjectName("mainTabsFontSizeSpinBox")
        self.gridlayout.addWidget(self.mainTabsFontSizeSpinBox,1,1,1,1)

        self.label = QtGui.QLabel(self.fontGroupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,2,0,1,1)

        self.generalTextFontSizeSpinBox = QtGui.QSpinBox(self.fontGroupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generalTextFontSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.generalTextFontSizeSpinBox.setSizePolicy(sizePolicy)
        self.generalTextFontSizeSpinBox.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.generalTextFontSizeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.generalTextFontSizeSpinBox.setObjectName("generalTextFontSizeSpinBox")
        self.gridlayout.addWidget(self.generalTextFontSizeSpinBox,2,1,1,1)
        self.vboxlayout.addWidget(self.fontGroupBox)

        self.prevProjPrefGroupBox = QtGui.QGroupBox(PreferencesDialog)
        self.prevProjPrefGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.prevProjPrefGroupBox.setFlat(False)
        self.prevProjPrefGroupBox.setCheckable(False)
        self.prevProjPrefGroupBox.setObjectName("prevProjPrefGroupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.prevProjPrefGroupBox)
        self.gridlayout1.setObjectName("gridlayout1")

        self.prevProjPrefCheckBox = QtGui.QCheckBox(self.prevProjPrefGroupBox)
        self.prevProjPrefCheckBox.setObjectName("prevProjPrefCheckBox")
        self.gridlayout1.addWidget(self.prevProjPrefCheckBox,0,0,1,1)
        self.vboxlayout.addWidget(self.prevProjPrefGroupBox)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.applyButton = QtGui.QPushButton(PreferencesDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applyButton.sizePolicy().hasHeightForWidth())
        self.applyButton.setSizePolicy(sizePolicy)
        self.applyButton.setAutoDefault(True)
        self.applyButton.setObjectName("applyButton")
        self.hboxlayout.addWidget(self.applyButton)

        self.okButton = QtGui.QPushButton(PreferencesDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.okButton.sizePolicy().hasHeightForWidth())
        self.okButton.setSizePolicy(sizePolicy)
        self.okButton.setAutoDefault(True)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)

        self.cancelButton = QtGui.QPushButton(PreferencesDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(PreferencesDialog)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialog)

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QtGui.QApplication.translate("PreferencesDialog", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.fontGroupBox.setTitle(QtGui.QApplication.translate("PreferencesDialog", "Font Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFontSizeLabel.setText(QtGui.QApplication.translate("PreferencesDialog", "Menu Bar Font Size", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabsFontSizeLabel.setText(QtGui.QApplication.translate("PreferencesDialog", "Main Tab Font Size", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesDialog", "General Text Font Size", None, QtGui.QApplication.UnicodeUTF8))
        self.prevProjPrefGroupBox.setTitle(QtGui.QApplication.translate("PreferencesDialog", "Previous Project Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.prevProjPrefCheckBox.setText(QtGui.QApplication.translate("PreferencesDialog", "Open previous project on startup", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtGui.QApplication.translate("PreferencesDialog", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("PreferencesDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("PreferencesDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

