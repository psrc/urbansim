# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xml_editor.ui'
#
# Created: Tue Dec 20 12:28:15 2011
#      by: PyQt5 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_XML_Editor(object):
    def setupUi(self, XML_Editor):
        XML_Editor.setObjectName(_fromUtf8("XML_Editor"))
        XML_Editor.resize(914, 598)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(XML_Editor.sizePolicy().hasHeightForWidth())
        XML_Editor.setSizePolicy(sizePolicy)
        XML_Editor.setWindowTitle(QtWidgets.QApplication.translate("XML_Editor", "XML Editor", None))
        XML_Editor.setLocale(QtCore.QLocale(QtCore.QLocale.German, QtCore.QLocale.Switzerland))
        self.gridLayout = QtWidgets.QGridLayout(XML_Editor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtWidgets.QTextEdit(XML_Editor)
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.revertButton = QtWidgets.QPushButton(XML_Editor)
        self.revertButton.setText(QtWidgets.QApplication.translate("XML_Editor", "Revert", None))
        self.revertButton.setObjectName(_fromUtf8("revertButton"))
        self.horizontalLayout.addWidget(self.revertButton)
        self.syntaxButton = QtWidgets.QPushButton(XML_Editor)
        self.syntaxButton.setText(QtWidgets.QApplication.translate("XML_Editor", "Syntax Check", None))
        self.syntaxButton.setObjectName(_fromUtf8("syntaxButton"))
        self.horizontalLayout.addWidget(self.syntaxButton)
        self.cancelButton = QtWidgets.QPushButton(XML_Editor)
        self.cancelButton.setText(QtWidgets.QApplication.translate("XML_Editor", "Cancel", None))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.okButton = QtWidgets.QPushButton(XML_Editor)
        self.okButton.setText(QtWidgets.QApplication.translate("XML_Editor", "OK", None))
        self.okButton.setDefault(True)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(XML_Editor)
        QtCore.QMetaObject.connectSlotsByName(XML_Editor)

    def retranslateUi(self, XML_Editor):
        pass

