# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/opus_trunk/opus_gui/main/views/log_widget.ui'
#
# Created: Sun May 10 12:41:21 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LogWidget(object):
    def setupUi(self, LogWidget):
        LogWidget.setObjectName("LogWidget")
        LogWidget.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(LogWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.te_logging = QtGui.QPlainTextEdit(LogWidget)
        self.te_logging.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.te_logging.setReadOnly(True)
        self.te_logging.setBackgroundVisible(False)
        self.te_logging.setObjectName("te_logging")
        self.verticalLayout.addWidget(self.te_logging)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_refresh = QtGui.QPushButton(LogWidget)
        self.pb_refresh.setObjectName("pb_refresh")
        self.horizontalLayout.addWidget(self.pb_refresh)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_save = QtGui.QPushButton(LogWidget)
        self.pb_save.setObjectName("pb_save")
        self.horizontalLayout.addWidget(self.pb_save)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LogWidget)
        QtCore.QMetaObject.connectSlotsByName(LogWidget)

    def retranslateUi(self, LogWidget):
        LogWidget.setWindowTitle(QtGui.QApplication.translate("LogWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_refresh.setText(QtGui.QApplication.translate("LogWidget", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_save.setText(QtGui.QApplication.translate("LogWidget", "Save output", None, QtGui.QApplication.UnicodeUTF8))

