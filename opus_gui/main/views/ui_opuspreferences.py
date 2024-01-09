# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opuspreferences.ui'
#
# Created: Wed Oct 01 08:21:12 2008
#      by: PyQt5 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName("PreferencesDialog")
        PreferencesDialog.resize(QtCore.QSize(QtCore.QRect(0,0,438,215).size()).expandedTo(PreferencesDialog.minimumSizeHint()))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PreferencesDialog.sizePolicy().hasHeightForWidth())
        PreferencesDialog.setSizePolicy(sizePolicy)

        self.vboxlayout = QtWidgets.QVBoxLayout(PreferencesDialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.fontGroupBox = QtWidgets.QGroupBox(PreferencesDialog)
        self.fontGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.fontGroupBox.setObjectName("fontGroupBox")

        self.gridlayout = QtWidgets.QGridLayout(self.fontGroupBox)
        self.gridlayout.setObjectName("gridlayout")

        self.menuFontSizeLabel = QtWidgets.QLabel(self.fontGroupBox)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuFontSizeLabel.sizePolicy().hasHeightForWidth())
        self.menuFontSizeLabel.setSizePolicy(sizePolicy)
        self.menuFontSizeLabel.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.menuFontSizeLabel.setObjectName("menuFontSizeLabel")
        self.gridlayout.addWidget(self.menuFontSizeLabel,0,0,1,1)

        self.menuFontSizeSpinBox = QtWidgets.QSpinBox(self.fontGroupBox)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuFontSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.menuFontSizeSpinBox.setSizePolicy(sizePolicy)
        self.menuFontSizeSpinBox.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.menuFontSizeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.menuFontSizeSpinBox.setObjectName("menuFontSizeSpinBox")
        self.gridlayout.addWidget(self.menuFontSizeSpinBox,0,1,1,1)

        self.mainTabsFontSizeLabel = QtWidgets.QLabel(self.fontGroupBox)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainTabsFontSizeLabel.sizePolicy().hasHeightForWidth())
        self.mainTabsFontSizeLabel.setSizePolicy(sizePolicy)
        self.mainTabsFontSizeLabel.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.mainTabsFontSizeLabel.setObjectName("mainTabsFontSizeLabel")
        self.gridlayout.addWidget(self.mainTabsFontSizeLabel,1,0,1,1)

        self.mainTabsFontSizeSpinBox = QtWidgets.QSpinBox(self.fontGroupBox)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainTabsFontSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.mainTabsFontSizeSpinBox.setSizePolicy(sizePolicy)
        self.mainTabsFontSizeSpinBox.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.mainTabsFontSizeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mainTabsFontSizeSpinBox.setObjectName("mainTabsFontSizeSpinBox")
        self.gridlayout.addWidget(self.mainTabsFontSizeSpinBox,1,1,1,1)

        self.label = QtWidgets.QLabel(self.fontGroupBox)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,2,0,1,1)

        self.generalTextFontSizeSpinBox = QtWidgets.QSpinBox(self.fontGroupBox)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generalTextFontSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.generalTextFontSizeSpinBox.setSizePolicy(sizePolicy)
        self.generalTextFontSizeSpinBox.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.generalTextFontSizeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.generalTextFontSizeSpinBox.setObjectName("generalTextFontSizeSpinBox")
        self.gridlayout.addWidget(self.generalTextFontSizeSpinBox,2,1,1,1)
        self.vboxlayout.addWidget(self.fontGroupBox)

        self.prevProjPrefGroupBox = QtWidgets.QGroupBox(PreferencesDialog)
        self.prevProjPrefGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.prevProjPrefGroupBox.setFlat(False)
        self.prevProjPrefGroupBox.setCheckable(False)
        self.prevProjPrefGroupBox.setObjectName("prevProjPrefGroupBox")

        self.gridlayout1 = QtWidgets.QGridLayout(self.prevProjPrefGroupBox)
        self.gridlayout1.setObjectName("gridlayout1")

        self.prevProjPrefCheckBox = QtWidgets.QCheckBox(self.prevProjPrefGroupBox)
        self.prevProjPrefCheckBox.setObjectName("prevProjPrefCheckBox")
        self.prevProjPrefCheckBox.setChecked(True)
        self.gridlayout1.addWidget(self.prevProjPrefCheckBox,0,0,1,1)
        
        self.prevProjPrefTabCheckBox = QtWidgets.QCheckBox(self.prevProjPrefGroupBox)
        self.prevProjPrefTabCheckBox.setObjectName("prevProjPrefTabCheckBox")
        self.gridlayout1.addWidget(self.prevProjPrefTabCheckBox,1,0,1,1)
        self.vboxlayout.addWidget(self.prevProjPrefGroupBox)

        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtWidgets.QSpacerItem(40,20,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.applyButton = QtWidgets.QPushButton(PreferencesDialog)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applyButton.sizePolicy().hasHeightForWidth())
        self.applyButton.setSizePolicy(sizePolicy)
        self.applyButton.setAutoDefault(True)
        self.applyButton.setObjectName("applyButton")
        self.hboxlayout.addWidget(self.applyButton)

        self.okButton = QtWidgets.QPushButton(PreferencesDialog)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.okButton.sizePolicy().hasHeightForWidth())
        self.okButton.setSizePolicy(sizePolicy)
        self.okButton.setAutoDefault(True)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)

        self.cancelButton = QtWidgets.QPushButton(PreferencesDialog)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
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
        PreferencesDialog.setWindowTitle(QtWidgets.QApplication.translate("PreferencesDialog", "Preferences", None, QtWidgets.QApplication.UnicodeUTF8))
        self.fontGroupBox.setTitle(QtWidgets.QApplication.translate("PreferencesDialog", "Font Preferences", None, QtWidgets.QApplication.UnicodeUTF8))
        self.menuFontSizeLabel.setText(QtWidgets.QApplication.translate("PreferencesDialog", "Menu Bar Font Size", None, QtWidgets.QApplication.UnicodeUTF8))
        self.mainTabsFontSizeLabel.setText(QtWidgets.QApplication.translate("PreferencesDialog", "Main Tab Font Size", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label.setText(QtWidgets.QApplication.translate("PreferencesDialog", "General Text Font Size", None, QtWidgets.QApplication.UnicodeUTF8))
        self.prevProjPrefGroupBox.setTitle(QtWidgets.QApplication.translate("PreferencesDialog", "Previous Project Preferences", None, QtWidgets.QApplication.UnicodeUTF8))
        self.prevProjPrefCheckBox.setText(QtWidgets.QApplication.translate("PreferencesDialog", "Open previous project on startup", None, QtWidgets.QApplication.UnicodeUTF8))
        self.prevProjPrefTabCheckBox.setText(QtWidgets.QApplication.translate("PreferencesDialog", "Activate previous tab on startup", None, QtWidgets.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtWidgets.QApplication.translate("PreferencesDialog", "Apply", None, QtWidgets.QApplication.UnicodeUTF8))
        self.okButton.setText(QtWidgets.QApplication.translate("PreferencesDialog", "OK", None, QtWidgets.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtWidgets.QApplication.translate("PreferencesDialog", "Cancel", None, QtWidgets.QApplication.UnicodeUTF8))

