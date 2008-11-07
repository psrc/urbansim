# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_indicator_batch.ui'
#
# Created: Fri Nov  7 10:01:08 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgAddIndicatorBatch(object):
    def setupUi(self, dlgAddIndicatorBatch):
        dlgAddIndicatorBatch.setObjectName("dlgAddIndicatorBatch")
        dlgAddIndicatorBatch.resize(417, 114)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgAddIndicatorBatch.sizePolicy().hasHeightForWidth())
        dlgAddIndicatorBatch.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(dlgAddIndicatorBatch)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(dlgAddIndicatorBatch)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.leBatchName = QtGui.QLineEdit(dlgAddIndicatorBatch)
        self.leBatchName.setObjectName("leBatchName")
        self.horizontalLayout.addWidget(self.leBatchName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(dlgAddIndicatorBatch)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dlgAddIndicatorBatch)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dlgAddIndicatorBatch.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dlgAddIndicatorBatch.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgAddIndicatorBatch)

    def retranslateUi(self, dlgAddIndicatorBatch):
        dlgAddIndicatorBatch.setWindowTitle(QtGui.QApplication.translate("dlgAddIndicatorBatch", "Add new indicator batch", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgAddIndicatorBatch", "Batch name:", None, QtGui.QApplication.UnicodeUTF8))
        self.leBatchName.setText(QtGui.QApplication.translate("dlgAddIndicatorBatch", "untitled_indicator_batch", None, QtGui.QApplication.UnicodeUTF8))

