# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ckla/Documents/workspace/variable_library_rewrite/opus_gui/general_manager/views/dependency_viewer.ui'
#
# Created: Fri May  8 19:54:37 2009
#      by: PyQt5 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_DependencyViewer(object):
    def setupUi(self, DependencyViewer):
        DependencyViewer.setObjectName("DependencyViewer")
        DependencyViewer.resize(579, 185)
        DependencyViewer.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(DependencyViewer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_error = QtWidgets.QLabel(DependencyViewer)
        self.lbl_error.setObjectName("lbl_error")
        self.verticalLayout.addWidget(self.lbl_error)
        self.scrollArea = QtWidgets.QScrollArea(DependencyViewer)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 551, 77))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(0, 0, 291, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.widget = QtWidgets.QWidget(DependencyViewer)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 45))
        self.widget.setObjectName("widget")
        self.hboxlayout = QtWidgets.QHBoxLayout(self.widget)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtWidgets.QSpacerItem(441, 24, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.closeWindow = QtWidgets.QPushButton(self.widget)
        self.closeWindow.setObjectName("closeWindow")
        self.hboxlayout.addWidget(self.closeWindow)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(DependencyViewer)
        QtCore.QMetaObject.connectSlotsByName(DependencyViewer)

    def retranslateUi(self, DependencyViewer):
        DependencyViewer.setWindowTitle(QtWidgets.QApplication.translate("DependencyViewer", "Variable editor", None, QtWidgets.QApplication.UnicodeUTF8))
        self.lbl_error.setText(QtWidgets.QApplication.translate("DependencyViewer", "You do not appear to have GraphViz installed. The visualization can not be shown.", None, QtWidgets.QApplication.UnicodeUTF8))
        self.closeWindow.setText(QtWidgets.QApplication.translate("DependencyViewer", "Close", None, QtWidgets.QApplication.UnicodeUTF8))

