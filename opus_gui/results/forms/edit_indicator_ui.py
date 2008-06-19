# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_indicator.ui'
#
# Created: Thu Jun 19 16:33:00 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgEditIndicator(object):
    def setupUi(self, dlgEditIndicator):
        dlgEditIndicator.setObjectName("dlgEditIndicator")
        dlgEditIndicator.resize(533, 234)
        self.layoutWidget = QtGui.QWidget(dlgEditIndicator)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 501, 186))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(-1, 20, -1, 20)
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.txtPackage_name = QtGui.QLineEdit(self.layoutWidget)
        self.txtPackage_name.setObjectName("txtPackage_name")
        self.gridLayout.addWidget(self.txtPackage_name, 1, 1, 1, 1)
        self.txtIndicator_name = QtGui.QLineEdit(self.layoutWidget)
        self.txtIndicator_name.setObjectName("txtIndicator_name")
        self.gridLayout.addWidget(self.txtIndicator_name, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.txtExpression = QtGui.QLineEdit(self.layoutWidget)
        self.txtExpression.setObjectName("txtExpression")
        self.gridLayout.addWidget(self.txtExpression, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(dlgEditIndicator)
        self.buttonBox.setGeometry(QtCore.QRect(290, 190, 233, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(dlgEditIndicator)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dlgEditIndicator.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dlgEditIndicator.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgEditIndicator)

    def retranslateUi(self, dlgEditIndicator):
        dlgEditIndicator.setWindowTitle(QtGui.QApplication.translate("dlgEditIndicator", "Indicator definition editor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgEditIndicator", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dlgEditIndicator", "Package (optional):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("dlgEditIndicator", "Expression:", None, QtGui.QApplication.UnicodeUTF8))

