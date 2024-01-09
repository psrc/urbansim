# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/travis/Documents/workspace/opus/opus_gui/results_manager/views/run_indicator_batch.ui'
#
# Created: Fri Sep 26 18:41:16 2008
#      by: PyQt5 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_runIndicatorBatch(object):
    def setupUi(self, runIndicatorBatch):
        runIndicatorBatch.setObjectName("runIndicatorBatch")
        runIndicatorBatch.resize(561, 109)
        self.gridlayout = QtWidgets.QGridLayout(runIndicatorBatch)
        self.gridlayout.setObjectName("gridlayout")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.label = QtWidgets.QLabel(runIndicatorBatch)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)
        self.co_start_year = QtWidgets.QComboBox(runIndicatorBatch)
        self.co_start_year.setObjectName("co_start_year")
        self.hboxlayout.addWidget(self.co_start_year)
        self.label_2 = QtWidgets.QLabel(runIndicatorBatch)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)
        self.co_end_year = QtWidgets.QComboBox(runIndicatorBatch)
        self.co_end_year.setObjectName("co_end_year")
        self.hboxlayout.addWidget(self.co_end_year)
        self.label_3 = QtWidgets.QLabel(runIndicatorBatch)
        self.label_3.setObjectName("label_3")
        self.hboxlayout.addWidget(self.label_3)
        self.co_every_year = QtWidgets.QComboBox(runIndicatorBatch)
        self.co_every_year.setObjectName("co_every_year")
        self.hboxlayout.addWidget(self.co_every_year)
        self.label_4 = QtWidgets.QLabel(runIndicatorBatch)
        self.label_4.setObjectName("label_4")
        self.hboxlayout.addWidget(self.label_4)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(runIndicatorBatch)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.NoButton|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(runIndicatorBatch)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("accepted()"), runIndicatorBatch.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("rejected()"), runIndicatorBatch.reject)
        QtCore.QMetaObject.connectSlotsByName(runIndicatorBatch)

    def retranslateUi(self, runIndicatorBatch):
        runIndicatorBatch.setWindowTitle(QtWidgets.QApplication.translate("runIndicatorBatch", "Run indicator batch", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label.setText(QtWidgets.QApplication.translate("runIndicatorBatch", "From", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label_2.setText(QtWidgets.QApplication.translate("runIndicatorBatch", "To", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label_3.setText(QtWidgets.QApplication.translate("runIndicatorBatch", "Every", None, QtWidgets.QApplication.UnicodeUTF8))
        self.label_4.setText(QtWidgets.QApplication.translate("runIndicatorBatch", "years", None, QtWidgets.QApplication.UnicodeUTF8))

