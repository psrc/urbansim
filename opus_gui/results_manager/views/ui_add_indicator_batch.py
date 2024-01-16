# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_indicator_batch.ui'
#
# Created: Fri Nov  7 10:01:08 2008
#      by: PyQt5 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_dlgAddIndicatorBatch(object):
    def setupUi(self, dlgAddIndicatorBatch):
        dlgAddIndicatorBatch.setObjectName("dlgAddIndicatorBatch")
        dlgAddIndicatorBatch.resize(417, 114)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgAddIndicatorBatch.sizePolicy().hasHeightForWidth())
        dlgAddIndicatorBatch.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(dlgAddIndicatorBatch)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(dlgAddIndicatorBatch)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.leBatchName = QtWidgets.QLineEdit(dlgAddIndicatorBatch)
        self.leBatchName.setObjectName("leBatchName")
        self.horizontalLayout.addWidget(self.leBatchName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgAddIndicatorBatch)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dlgAddIndicatorBatch)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("accepted()"), dlgAddIndicatorBatch.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("rejected()"), dlgAddIndicatorBatch.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgAddIndicatorBatch)

    def retranslateUi(self, dlgAddIndicatorBatch):
        dlgAddIndicatorBatch.setWindowTitle(QtWidgets.QApplication.translate("dlgAddIndicatorBatch", "Add new indicator batch", None))
        self.label.setText(QtWidgets.QApplication.translate("dlgAddIndicatorBatch", "Batch name:", None))
        self.leBatchName.setText(QtWidgets.QApplication.translate("dlgAddIndicatorBatch", "untitled_indicator_batch", None))

