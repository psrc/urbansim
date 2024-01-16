# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/travis/Documents/workspace/opus/opus_gui/results_manager/views/import_run_dialog.ui'
#
# Created: Fri Sep 26 18:36:35 2008
#      by: PyQt5 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_dlgImportRun(object):
    def setupUi(self, dlgImportRun):
        dlgImportRun.setObjectName("dlgImportRun")
        dlgImportRun.resize(600, 117)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgImportRun.sizePolicy().hasHeightForWidth())
        dlgImportRun.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgImportRun)
        self.buttonBox.setGeometry(QtCore.QRect(240, 70, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(dlgImportRun)
        self.widget.setGeometry(QtCore.QRect(10, 10, 561, 41))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblOption1 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblOption1.sizePolicy().hasHeightForWidth())
        self.lblOption1.setSizePolicy(sizePolicy)
        self.lblOption1.setObjectName("lblOption1")
        self.horizontalLayout.addWidget(self.lblOption1)
        self.lePath = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lePath.sizePolicy().hasHeightForWidth())
        self.lePath.setSizePolicy(sizePolicy)
        self.lePath.setMinimumSize(QtCore.QSize(100, 0))
        self.lePath.setObjectName("lePath")
        self.horizontalLayout.addWidget(self.lePath)
        self.pbn_set_run_directory = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbn_set_run_directory.sizePolicy().hasHeightForWidth())
        self.pbn_set_run_directory.setSizePolicy(sizePolicy)
        self.pbn_set_run_directory.setObjectName("pbn_set_run_directory")
        self.horizontalLayout.addWidget(self.pbn_set_run_directory)

        self.retranslateUi(dlgImportRun)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("accepted()"), dlgImportRun.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.pyqtSignal("rejected()"), dlgImportRun.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgImportRun)

    def retranslateUi(self, dlgImportRun):
        dlgImportRun.setWindowTitle(QtWidgets.QApplication.translate("dlgImportRun", "Import run from disk", None))
        self.lblOption1.setText(QtWidgets.QApplication.translate("dlgImportRun", "Path to run directory:", None))
        self.pbn_set_run_directory.setText(QtWidgets.QApplication.translate("dlgImportRun", "...", None))

